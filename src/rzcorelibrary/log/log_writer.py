# File Name: rz-core-libarary/src/rzcorelibrary/log/log_writer.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ...plugins.base import BasePlugin

import inspect
import traceback
from pathlib import Path
import os
import re

class LogWriter:

    FULL_CLASS_NAME = "LogWriter"
    CLASS_NAME = "LogWriter"
    DEBUG_PREFIX = "DEBUG_LOG_WRITER_PRINT: "
    stack_trace_lines = None

    def __init__(self):
        raise TypeError(
            f"{self.__class__.__name__} cannot be instantiated."
        )

    @staticmethod
    def log(message: str = "", is_debug: bool = True):
        """
        Logs message with caller info.
        """
        if not is_debug:
            return

        caller_info = LogWriter._log_caller()
        if caller_info:
            message = f"{message} {caller_info}"

        print(f"{LogWriter.DEBUG_PREFIX}{message}")

    @staticmethod
    def _log_caller():
        """
        Returns caller info from stack trace.
        """
        trace_lines = LogWriter._get_stack_trace_lines()

        # Find first line that is outside LogWriter itself
        """for line in trace_lines:
            if LogWriter.CLASS_NAME not in line:
                return line.strip()"""
        
        current_file_path = os.path.abspath(__file__)
        #print(trace_list)
        index = 0
        counter = 0
        #print("---------------")
        '''for line in trace_lines:
            index += 1
            if current_file_path in line:
                counter += 1
                continue
            if(index > counter):
                break;'''
        for line in trace_lines:
            if current_file_path in line:
                break
            index += 1
        index -= 1
        trace_line = ""
        #print("index: ", index)
        if index >= 0 and index < len(trace_lines):
            trace_line = trace_lines[index]
            #print(trace_line)
        match = re.search(r'File "(.+?)", line (\d+)', trace_line)
        if match:
            file_path = match.group(1)
            line_no = match.group(2)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            #print("file path: " + file_name + ", line no: " + line_no)
            return f"{file_name} - line {line_no}"

        return None

    @staticmethod
    def _get_stack_trace_lines():
        """
        Returns stack trace lines excluding current function.
        """
        trace = traceback.format_stack()
        trace_list = []
        for line in trace:
            trace_list.extend(line.split('\n'))
        # Remove empty strings
        trace_list = [line for line in trace_list if line.strip()]
        #trace_list.reverse()
        """#current_file_path = Path(__file__).resolve()
        current_file_path = os.path.abspath(__file__)
        #print(trace_list)
        index = 0
        counter = 0
        print("---------------")
        for line in trace_list:
            index += 1
            if current_file_path in line:
                counter += 1
                continue
            if(counter > index):
                break;
        print(current_file_path)"""
        #trace = traceback.format_exc()
        #trace_list = [line.strip().split() for line in trace]
        #trace_list = trace.split('\n')
        #print(trace_list)
        LogWriter.stack_trace_lines = trace_list
        return trace

    @staticmethod
    def get_full_stack_line():
        """
        Returns the first line containing file info.
        """
        for line in LogWriter._get_stack_trace_lines():
            if "File" in line:
                return line.strip()
        return None

    @staticmethod
    def get_file_name():
        """
        Returns the current file name from the stack trace.
        """
        frame = inspect.currentframe()
        if frame is None:
            return None

        caller_frame = frame.f_back
        if caller_frame is None:
            return None

        filename = caller_frame.f_code.co_filename
        return filename.split("/")[-1]

class Plugin(BasePlugin):
    name = "log_writer"
    version = "1.0.0"
    description = "Log writer utility"
    def get_util(self):
        return LogWriter