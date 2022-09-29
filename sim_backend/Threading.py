"""
Backend - Threading Classes
Created on Mon February 28, 2022

Summary: The Threading classes provide a high level interface for running functions on a
         separate thread of execution. The SIMThread class takes in a specific Worker type and function
         and executes that function according to the rules of the given worker. A ThreadWorker will
         execute the function once, and exposes a signal that can call a secondary function when the
         initial function finishes. A SignaledWorker will execute the function whenever it is signaled.
         This signal can be sent multiple times.

References:
    None

Referenced By:
    Experiment
    MapExplorationExperiment
    TestExperiment

"""

# Library Imports
import logging
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from typing import Callable


class ThreadWorker(QObject):

    # The signals that can be connected to slots on another thread
    finished: pyqtSignal = pyqtSignal(bool)

    def __init__(self, function: Callable, *args):
        # Call the base QObject constructor
        super(ThreadWorker, self).__init__()

        # This function is the one that the Thread will execute when run
        self.function: Callable = function

        # Store the args that need to be passed to the called function
        self.args = args

    def call_when_finished(self, function: Callable) -> None:
        """
        Allows the user to specify a second function that will be called when the thread finishes.

        The function pass in here will be triggered on the main thread whenever this worker has
        finished. For a ThreadWorker, this second function will run once the main function has
        run once. For a RepeatedWorker, this second function will run once the worker has been
        stopped manually. This secondary function can only take a single bool as a parameter. The
        worker will pass the success status of the main function as a parameter into this secondary
        function.

        :param function: the function object to be run when the worker exits
        :return: None
        """

        self.finished.connect(function)

    def run(self) -> None:
        """
        The main function that will execute on another thread.

        Provides an error-handling wrapper around the main function, and signals the finishing
        state of the function when it exits.

        :return: None
        """

        try:
            # Run the provided function
            self.function(*self.args)
            # Signal to any connected slots that the function ran successfully
            self.finished.emit(True)

        except Exception as e:
            # Signal to any connected slots that the function did not run successfully
            logging.error(e)
            self.finished.emit(False)


class SIMThread:

    def __init__(self, thread_worker: ThreadWorker, mode: str = "single") -> None:
        # Initialize a QThread to run the function on
        self.thread: QThread = QThread()

        # Mode that the ThreadWorker will be set up to run in
        if mode not in ["single", "signaled"]:
            raise Exception("Unsupported mode passed into SIMThread constructor.")
        self.mode = mode

        # Store the provided worker
        self.worker: ThreadWorker = thread_worker

        # Start executing the worker on the second thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        if mode == "single":
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def signal_worker(self) -> None:
        """
        Signals the thread worker to run the function again.

        If the SimThread is configured to run in "signaled" mode, then it's function will run
        every time that this function is called. If the SimThread is configured to run in "single"
        mode, then calling this function will have no effect

        :return:
        """

        if self.mode == "single":
            return
        self.thread.started.emit()

    def destroy_thread(self) -> None:
        """
        Function to clean up after a SIMThread is done being used.

        If called on a SIMThread that is configured for "single" mode, nothing will happen as the
        thread will take care of everything once it finishes execution. If called on a SIMThread that
        is configured for "signaled" mode, the thread will be killed and its worker and object will
        be finalized

        :return: None
        """

        if self.mode == "single":
            return
        self.thread.quit()
        self.worker.deleteLater()
        self.thread.deleteLater()


class HeadlessWindow(QMainWindow):
    """
    QMainWindow that can be used when the Application is run in headless mode.

    A QApplication must be running for the QThreads to operate as expected. Therefore, when an Experiment
    script needs to be run without the main GUI (likely for testing purposes) this class needs to be instantiated
    so everything can run like it normally would with the GUI.
    """
    def __init__(self, function: Callable, parent=None) -> None:

        # Run the QMainWindow constructor
        super().__init__(parent)

        # Run the function that was passed in
        function()
