import functools
import logging
import time

MODULE_LOGGER = logging.getLogger("Textual")


def timer(*, level: int = logging.INFO, precision: int = 4):
    """
    Print the runtime of the decorated function.

    Args:
        level: the logging level for the time message [default=INFO]
        precision: the number of decimals for the time [default=3 (ms)]
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            MODULE_LOGGER.log(level, f"Finished {func.__name__!r} in {run_time:.{precision}f} secs")
            return value

        return wrapper_timer
    return actual_decorator


def do_every(period: float, func: callable, *args) -> None:
    """

    This method executes a function periodically, taking into account
    that the function that is executed will take time also and using a
    simple `sleep()` will cause a drift. This method will not drift.

    You can use this function in combination with the threading module to execute the
    function in the background, but be careful as the function might not be thread safe.

    ```
    timer_thread = threading.Thread(target=do_every, args=(10, func))
    timer_thread.daemon = True
    timer_thread.start()
    ```

    Args:
        period: a time interval between successive executions [seconds]
        func: the function to be executed
        *args: optional arguments to be passed to the function
    """

    # Code from SO:https://stackoverflow.com/a/28034554/4609203
    # The max in the yield line serves to protect sleep from negative numbers in case the
    # function being called takes longer than the period specified. In that case it would
    # execute immediately and make up the lost time in the timing of the next execution.

    def g_tick():
        next_time = time.time()
        while True:
            next_time += period
            yield max(next_time - time.time(), 0)

    g = g_tick()
    while True:
        time.sleep(next(g))
        func(*args)
