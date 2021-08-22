"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/18/2021

Purpose:

Details:

Description:

Notes:
    The Traversal is the the preorder traversal if that helps
        (Root, Left, Right)

IMPORTANT NOTES:
    THIS PROGRAM WILL NOT HANDLE UTF-8 CHARS THAT HAVE > 1 BYTE, SO ONLY ASCII CHARS THAT ARE EITHER INTEGERS OR A
    COMMA.

    FILE CONTENTS MUST BE IN THESE CORRECT FORMS:
        INT,INT,INT
        INT

    FILE CONTENTS CANNOT BE IN THIS FORM:
        ,
        INT,
        ,INT
        INT,,INT

Explanation:


Reference:
    Why Is Merge Sort O(n * log(n))? The Really Really Long Answer.
        Reference:
            https://www.youtube.com/watch?v=alJswNJ4P3U

    geohot / mergesorts
        Reference:
            https://github.com/geohot/mergesorts/blob/master/mergesort.py

"""
import traceback
import warnings
from functools import wraps
from pprint import pprint
from typing import Dict, Union, List, Tuple

# from pycode_recorder.algorithm_recorder import AlgorithmRecorder
# from joseph_resources.decorators.callgraph_simple import create_callgraph, callgraph

# algorithm_recorder = AlgorithmRecorder()

_counter_read = 0
_counter_write = 0
_counter_flush_to_file = 0

DELIMITER = ","
BUFFER_SIZE_INPUT = 4096
BUFFER_SIZE_OUTPUT = 4096
DIRECTORY_CURRENT_WORKING: Dict[str, str] = {}


def _debugging_decorator(callable=None, debug_vars=True):
    """
    A Decorator to debug function

    """

    def _debugging_decorator_inner(callable):

        @wraps(callable)
        def wrapper(*args, **kwargs):
            print(f"{'#' * 100} {callable.__name__} {'#' * 100}")
            str_temp = f"{'=' * 25} args and kwargs {'=' * 25}"

            if debug_vars:
                print(str_temp)
                print("args:")
                pprint(args, indent=4)
                print()
                print("kwargs:")
                pprint(kwargs, indent=4)
                print()

            result = callable(*args, **kwargs)

            if debug_vars:
                print("result:")
                pprint(result, indent=4)
                print("=" * len(str_temp))

            return result

        return wrapper

    return _debugging_decorator_inner(callable) if callable else _debugging_decorator_inner


class Buffer(list):
    def __init__(self, name, size_buffer_max):
        seq = [None] * size_buffer_max
        super().__init__(seq)
        self._size_buffer_max = size_buffer_max
        self._name = name

    def get_size_buffer_max(self):
        return self._size_buffer_max

    def append(self, __object) -> None:
        # If your new length will be more than your max, then don't add
        if len(self) + 1 > self._size_buffer_max:
            print(f"BUFFER {self._name} IS FULL, CANNOT TAKE IN {__object}")
            return

        super(Buffer, self).append(__object)


BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)


# class FileData:
#     """
#     NOT USED, WILL USE UP MEMORY
#
#     """
#
#     def __init__(self, filename: str, amount_bytes: int, amount_int: int):
#         self.filename = filename,
#         self.amount_bytes = amount_bytes
#         self.amount_int = amount_int
#

# class FileContainer:
#     """
#     NOT USED, WILL USE UP MEMORY
#
#     """
#
#     def __init__(self):
#         self.list_filename_left: List[FileData] = []
#         self.list_filename_right: List[FileData] = []
#
#     def yield_filename_left(self):
#         for i in self.list_filename_left:
#             yield i
#
#     def yield_filename_right(self):
#         for i in self.list_filename_right:
#             yield i

# @callgraph
def read(filename: str, buffer: Buffer, index_file_starting: int, index_buffer_starting: int,
         amount_bytes_write_to_buffer) -> int:
    """
    FROM FILE TO BUFFER

    IMPORTANT NOTES:
        WILL CRASH IF YOU GO OUT OF BOUNDS FOR INDICES, I'M NOT GOING TO HANDLE THAT

    :return: Amount of bytes written to buffer
    """
    global _counter_read
    _counter_read += 1

    # list_int = [int(i) for i in DIRECTORY_CURRENT_WORKING.get(list_tuple_filename_bytes).split(DELIMITER)]
    #
    # for i in range(len(buffer)):
    #     buffer[i] = list_int[i]

    str_file_contents = DIRECTORY_CURRENT_WORKING.get(filename)

    index_file_starting_condition = False

    amount_bytes_written_to_buffer = 0

    index_file_current = 0

    if index_buffer_starting + 1 > buffer.get_size_buffer_max():
        return 0

    try:
        while True:

            # If fulfilled amount of bytes written to buffer
            if amount_bytes_written_to_buffer == amount_bytes_write_to_buffer:
                return amount_bytes_written_to_buffer

            # If index_file_current + 1 is END OF FILE (EOF)
            elif index_file_current + 1 > len(str_file_contents):
                return amount_bytes_written_to_buffer

            # If index_buffer_starting + 1 is bigger than the buffer size
            elif index_buffer_starting + 1 > buffer.get_size_buffer_max():
                return amount_bytes_written_to_buffer

            # Determine when to start reading from file to buffer
            if index_file_current == index_file_starting:
                index_file_starting_condition = True

            # Read from file to buffer
            if index_file_starting_condition:
                # print(f"-------------------{index_file_current=}")
                # print(str_file_contents)
                # print(f"-------------------{index_buffer_starting=}")

                buffer[index_buffer_starting] = str_file_contents[index_file_current]
                index_buffer_starting += 1
                amount_bytes_written_to_buffer += 1

            index_file_current += 1
    except Exception as e:
        print(e)
        return -1


# @callgraph
def write(filename: str, buffer: Buffer, delimiter: str = DELIMITER, append: bool = False) -> int:
    """
    FROM BUFFER TO FILENAME

    Notes:
        NOT IN C STYLE, BU SHOULD BE Theta(n)

    """
    global _counter_write
    _counter_write += 1

    string = "{}".format(delimiter).join([str(i) for i in buffer])

    if append:
        DIRECTORY_CURRENT_WORKING[filename] += delimiter + string
        return len(delimiter + string)
    else:
        DIRECTORY_CURRENT_WORKING[filename] = string
        return len(string)


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def get_amount_int_in_file(filename: str, buffer_temp: Buffer) -> int:
    """
    Get the amount of ints given the list_tuple_filename_bytes

    IMPORTANT NOTES:
        WILL CRASH IF
            YOU HAVE AN IMPROPER STRING
            STRING OF INT IS BIGGER THAN BUFFER SIZE

    :return: amount_of_int
    """

    # print(
    #     f"{get_amount_int_in_file.__name__}\n"
    #     f"{filename}\n"
    #     f"{DIRECTORY_CURRENT_WORKING[filename]}\n"
    # )

    index_buffer_input_temp = 0

    index_file_current = 0

    amount_of_int = 0

    while True:

        # DEBUGGING
        # print("---------------------")
        # print(f"{filename=}\n{buffer_temp=}\n{index_file_current=}\n{index_buffer_input_temp=}")
        # print("---------------------")

        """
        Check if buffer_temp is full

        This means that the char, that makes up the int, exceeds the buffer size.
        Basically, the int you are trying to make is TOO BIG for the buffer to make

        """
        if index_buffer_input_temp + 1 > buffer_temp.get_size_buffer_max():
            traceback.print_exc()
            warnings.warn("THIS INTEGER YOU ARE MAKING MIGHT BE TOO BIG TO FIT IN THE BUFFER")
            exit(1)

        """ #################### FROM FILE MAIN TO BUFFER INPUT #################### """

        """
        Assuming that index_buffer_input_temp is NOT FULL, then call the read function
        """

        """
        Add char from File to buffer_temp, return amount of bytes written to buffer
        """
        amount_bytes_written_to_buffer_input_left = read(filename,
                                                         buffer_temp,
                                                         index_file_current,
                                                         index_buffer_input_temp,
                                                         1)

        # amount_of_bytes_written == 0 then you are out of bounds implying that you are at the end of the file
        if amount_bytes_written_to_buffer_input_left == 0:

            # Increment amount of ints
            amount_of_int += 1

            return amount_of_int

        # Check if index_buffer_input_temp in buffer_temp is ","
        elif buffer_temp[index_buffer_input_temp] == DELIMITER:

            # Increment amount of ints
            amount_of_int += 1

            # Reset index for index_buffer_input_temp

            index_buffer_input_temp = 0
        else:
            index_buffer_input_temp += 1

        index_file_current += 1

    # ALTERNATIVE PYTHONIC WAY
    # return len([i for i in DIRECTORY_CURRENT_WORKING.get(list_tuple_filename_bytes).split(DELIMITER)])


# _id_unique = -1
# def _get_unique_id():
#     global _id_unique
#     _id_unique += 1
#     return _id_unique
#
#
# def _get_filename_current_instance(filename_current: str, index_file_partition):
#     return "{}_{}_{}.txt".format(filename_current, index_file_partition, _get_unique_id())


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def flush_to_file(filename: str, buffer: Buffer) -> Tuple[int, str]:
    """
    Flush the buffer into the file

    :return: amount_of_bytes_written, filename_returned
    """
    global _counter_flush_to_file
    _counter_flush_to_file += 1

    # filename = "{}_{}.txt".format(filename.replace(".txt", ""), _get_unique_id())

    filename_returned = None

    if DIRECTORY_CURRENT_WORKING.get(filename) is None:
        amount_of_bytes_written = write(filename, buffer)
        filename_returned = filename
    else:
        amount_of_bytes_written = write(filename, buffer,
                                        append=True)

    return amount_of_bytes_written, filename_returned


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def split_file_to_files(filename: str,
                        filename_base: str,
                        buffer_output: Buffer,
                        buffer_temp: Buffer,
                        amount_bytes_per_temp_file_max: Union[int, None] = None,
                        _index_stack_frame: int = 0,
                        ) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    """
    IMPORTANT NOTES:
        WILL CRASH IF
            YOU HAVE AN IMPROPER STRING
            STRING OF INT IS BIGGER THAN BUFFER SIZE

    :return:
    """

    # Amount of ints in the file using the buffer as memory
    amount_int_in_file = get_amount_int_in_file(filename, buffer_temp)

    # Amount of ints for the left size of the split
    amount_int_for_side_left = amount_int_in_file // 2

    filename_left = "{}_{}_{}_{}".format(filename_base.replace(".txt", ""), "split", _index_stack_frame, "L")
    filename_right = "{}_{}_{}_{}".format(filename_base.replace(".txt", ""), "split", _index_stack_frame, "R")

    filename_current = filename_left

    list_filename_left: List[Tuple[str, int]] = []

    list_filename_right: List[Tuple[str, int]] = []

    list_filename_current: List[Tuple[str, int]] = list_filename_left

    condition_run_once = False

    index_buffer_output = 0  #

    # Also the amount of bytes written to the buffer_temp
    index_buffer_temp = 0

    index_file_current = 0

    amount_bytes_char_buffer_temp_written_to_previous = 0

    amount_bytes_char_buffer_temp_used = 0  # Amount of bytes currently in use by buffer_temp

    amount_bytes_char_buffer_output_used = 0  # Amount of bytes currently in use by buffer_output

    amount_bytes_char_file_partition_written_to = 0  # Amount of bytes currently in current file_partition

    amount_int_buffer_output_seen = 0  # Amount of ints total that were in the the buffer

    amount_int_buffer_output = 0  # Amount of ints in the Output Buffer

    index_file_partition = 0  # Partition index

    while True:

        # DEBUGGING
        # print("---------------------")
        # print(
        #     # f"{list_tuple_filename_bytes=}\n"
        #     f"{buffer_temp=}\n"
        #     f"{buffer_output=}\n"
        #     f"{index_file_partition}"
        #     f"{index_buffer_output=}\n"
        #     f"{index_buffer_temp=}\n"
        #     f"{amount_int_buffer_output_seen=}\n"
        #     f"{amount_int_for_side_left=}\n"
        #     f"{amount_bytes_char_buffer_output_used=}\n"
        #     f"{amount_bytes_char_file_partition_written_to=}\n"
        #     f"{amount_bytes_char_buffer_temp_used=}\n"
        #
        # )
        # print("---------------------")

        # Check if the amount of ints is greater than the amount of ints that should be in the LEFT FILE
        if not condition_run_once and amount_int_buffer_output_seen >= amount_int_for_side_left:

            filename_current_instance = "{}_{}.txt".format(filename_current, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_current, index_file_partition)

            # If the output buffer has stuff in it
            if index_buffer_output != 0:

                # print(f"Flush: Switching from Left file to Right file\n"
                #       f"\t{amount_bytes_char_buffer_temp_written_to_previous=}\n"
                #       f"\t{buffer_output=}"
                #       f"\t{buffer_temp=}"
                #       f"\t{index_buffer_output}\n"
                #       )

                # Flush
                amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                    filename_current_instance,
                    buffer_output[0:index_buffer_output])

                # Increment amount of bytes to amount_bytes_char_file_partition_written_to
                amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

                if filename_current_instance_returned is not None:
                    list_filename_current.append((filename_current_instance,
                                                  amount_bytes_char_file_partition_written_to))
                else:
                    list_filename_current[index_file_partition] = (filename_current_instance,
                                                                   amount_bytes_char_file_partition_written_to)

                # Reset amount of ints in buffer_output
                amount_int_buffer_output = 0

                # Reset amount of bytes written to file
                amount_bytes_char_file_partition_written_to = 0

                # Reset amount of bytes in char form in output buffer
                amount_bytes_char_buffer_output_used = 0

            # Switch to file right side filename
            filename_current = filename_right

            # Switch to the right side list of filenames
            list_filename_current = list_filename_right

            # Reset index for file partition
            index_file_partition = 0

            # Reset index in index_buffer_output
            index_buffer_output = 0

            # Reset the amount of integers seen in buffer_output
            amount_int_buffer_output_seen = 0

            # Run this conditional once!
            condition_run_once = True

        """
        Check if buffer_temp is full

        This means that the char, that makes up the int, exceeds the buffer size.
        Basically, the int you are trying to make is TOO BIG for the buffer to make

        """
        if index_buffer_temp + 1 > buffer_temp.get_size_buffer_max():
            traceback.print_exc()
            warnings.warn("THIS INTEGER YOU ARE MAKING MIGHT BE TOO BIG TO FIT IN THE BUFFER")
            exit(1)

        """ 
        #################### FROM FILE TO BUFFER INPUT & BUFFER INPUT TO BUFFER OUTPUT #################### 
        Assuming that index_buffer_temp is NOT FULL, then call the read function
        """

        """
        Add char from File to buffer_temp, return amount of bytes written to buffer
        
        Notes:
            The read function should mimic C's read system call 
            
        """
        amount_bytes_char_buffer_temp_written_to = read(filename,
                                                        buffer_temp,
                                                        index_file_current,
                                                        index_buffer_temp,
                                                        1)

        amount_bytes_char_buffer_temp_used += amount_bytes_char_buffer_temp_written_to

        """
        If amount_bytes_char_buffer_temp_written_to == 0 
        then you are out of bounds implying that you are at the end of the file
        """

        if amount_bytes_char_buffer_temp_written_to == 0:

            # Buffer input to buffer output
            buffer_output[index_buffer_output] = int("".join(buffer_temp[0:index_buffer_temp]))

            # Increment index for index_buffer_output
            index_buffer_output += 1

            # Increment the amount of integers seen in buffer_output
            amount_int_buffer_output_seen += 1

            # Increment the amount of ints in buffer_output
            amount_int_buffer_output += 1

            # Increment amount of bytes in char form used in the output buffer
            amount_bytes_char_buffer_output_used += index_buffer_temp

            # Reset index for index_buffer_temp
            index_buffer_temp = 0

            # Rest amount_bytes_char_buffer_temp_used
            amount_bytes_char_buffer_temp_used = 0

            # print(f"Flush: EOF\n"
            #       f"\t{amount_bytes_char_buffer_temp_written_to_previous=}\n"
            #       f"\t{buffer_output=}\n"
            #       f"\t{buffer_temp=}\n"
            #       f"\t{index_buffer_output=}\n"
            #       )

            filename_current_instance = "{}_{}.txt".format(filename_current, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_current, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                filename_current_instance,
                buffer_output[0:index_buffer_output]
            )

            # Increment amount of bytes to amount_bytes_char_file_partition_written_to
            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            if filename_current_instance_returned is not None:
                list_filename_current.append((filename_current_instance,
                                              amount_bytes_char_file_partition_written_to))
            else:
                list_filename_current[index_file_partition] = (filename_current_instance,
                                                               amount_bytes_char_file_partition_written_to)

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

            # Reset amount of bytes written to file partition
            amount_bytes_char_file_partition_written_to = 0

            # Reset amount of bytes in char form in output buffer
            amount_bytes_char_buffer_output_used = 0

            break

        # Check if index_buffer_temp in buffer_temp is ","
        elif buffer_temp[index_buffer_temp] == DELIMITER:

            # atoi (ascii to int) operation on buffer_temp into buffer_output
            buffer_output[index_buffer_output] = int("".join(buffer_temp[0:index_buffer_temp]))

            # Increment index for index_buffer_output
            index_buffer_output += 1

            # Increment the amount of integers seen in buffer_output
            amount_int_buffer_output_seen += 1

            # Increment the amount of ints in buffer_output
            amount_int_buffer_output += 1

            # Increment amount of bytes in char form used in the output buffer
            amount_bytes_char_buffer_output_used += index_buffer_temp

            # Reset index for index_buffer_temp
            index_buffer_temp = 0

            # Rest amount_bytes_char_buffer_temp_used
            amount_bytes_char_buffer_temp_used = 0

        else:
            index_buffer_temp += 1

        # print(
        #     f"HERE:\n"
        #     f"{amount_bytes_char_file_partition_written_to=}\n"
        #     f"{amount_bytes_char_buffer_temp_used=}\n"
        #     f"{amount_bytes_char_buffer_output_used=}\n"
        #     f"{amount_int_buffer_output_seen=}\n"
        #     f"{index_buffer_output=}\n"
        #     f"{amount_bytes_per_temp_file_max=}\n"
        # )

        """ #################### FROM BUFFER OUTPUT TO FILE #################### """

        """
        Handle if amount of bytes per file partition
        
        Notes:
            # When the the Amount of bytes you have in the file + Amount of bytes you have in you INPUT Buffer EXCEEDS
            # the Maximum Amount of bytes for Temp File AND when the output buffer has nothing in it.
            
            OR
            
            (
            Amount of bytes char type written to the partitioned file +
            Amount of bytes char type in the Input buffer used +
            Amount of bytes char type in the Output buffer used +
            Amount of bytes char type written to the partitioned file that are delimiters
            ) > = Maximum Amount of bytes per temp file AND Output Buffer is empty
        
        
        """
        amount_bytes_char_file_partition_delimiter = (
                ((amount_int_buffer_output - 1) * len(DELIMITER) if amount_int_buffer_output > 1 else 0) +
                (len(DELIMITER) if amount_bytes_char_file_partition_written_to > 0 else 0)
        )

        # print(f"{amount_bytes_char_file_partition_delimiter=}")

        if (amount_bytes_per_temp_file_max is not None and
                (
                        # ((amount_bytes_char_file_partition_written_to +
                        #   amount_bytes_char_buffer_temp_used) > amount_bytes_per_temp_file_max and
                        #   amount_int_buffer_output != 0) or
                        ((amount_bytes_char_file_partition_written_to +
                          amount_bytes_char_buffer_temp_used +
                          amount_bytes_char_buffer_output_used +
                          amount_bytes_char_file_partition_delimiter
                         ) >= amount_bytes_per_temp_file_max and amount_int_buffer_output != 0)
                )

        ):

            # print(f"Flush: limited by bytes_per_temp_file_max\n"
            #       f"\t{amount_bytes_char_file_partition_written_to=}\n"
            #       f"\t{amount_bytes_char_buffer_temp_used=}\n"
            #       f"\t{buffer_output=}\n"
            #       f"\t{buffer_temp=}\n"
            #       f"\t{index_buffer_output=}\n"
            #       )

            filename_current_instance = "{}_{}.txt".format(filename_current, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_current, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned, = flush_to_file(
                filename_current_instance,
                buffer_output[0:index_buffer_output])

            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            if filename_current_instance_returned is not None:
                list_filename_current.append((filename_current_instance,
                                              amount_bytes_char_file_partition_written_to))
            else:
                list_filename_current[index_file_partition] = (filename_current_instance,
                                                               amount_bytes_char_file_partition_written_to)

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

            # Reset amount of bytes written to file partition
            amount_bytes_char_file_partition_written_to = 0

            # Reset amount of bytes in char form in output buffer
            amount_bytes_char_buffer_output_used = 0

            # Reset the index for index_buffer_output
            index_buffer_output = 0

            # Increment the index for the file partition
            index_file_partition += 1

        # Check if buffer_output is full (Flush buffer_output to file if full)
        elif index_buffer_output + 1 > buffer_output.get_size_buffer_max():
            # print(f"Flush: limited by buffer_output.get_size_buffer_max()\n"
            #       f"\t{buffer_output=}\n"
            #       f"\t{buffer_temp=}\n"
            #       f"\t{index_buffer_output=}\n"
            #       )

            filename_current_instance = "{}_{}.txt".format(filename_current, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_current, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                filename_current_instance,
                buffer_output)

            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            if filename_current_instance_returned is not None:
                list_filename_current.append((filename_current_instance,
                                              amount_bytes_char_file_partition_written_to))
            else:
                list_filename_current[index_file_partition] = (filename_current_instance,
                                                               amount_bytes_char_file_partition_written_to)

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

            # Reset amount of bytes written to file partition
            amount_bytes_char_file_partition_written_to = 0

            # Reset amount of bytes in char form in output buffer
            amount_bytes_char_buffer_output_used = 0

            # Reset the index for index_buffer_output
            index_buffer_output = 0

        amount_bytes_char_buffer_temp_written_to_previous = amount_bytes_char_buffer_temp_written_to

        index_file_current += 1

    # print(f"{split_file_to_files.__name__} Deleting:", filename)
    del DIRECTORY_CURRENT_WORKING[filename]
    return list_filename_left, list_filename_right


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def fill_int_buffer(filename: str,
                    buffer_output: Buffer,
                    buffer_temp: Buffer,
                    index_file_current: int) -> Tuple[int, int]:
    """
    FROM FILE TO BUFFER

    Notes:
        Modified fill buffer from split_file_to_files

    :return: amount_int_buffer_output_given, amount_bytes_char_buffer_temp_written_to_total
    """
    index_buffer_output_given = 0

    index_buffer_temp_given = 0

    amount_int_buffer_output_given = 0

    amount_bytes_char_buffer_temp_written_to_total = 0

    while True:
        """ 
        #################### FROM FILE TO BUFFER INPUT & BUFFER INPUT TO BUFFER OUTPUT #################### 
        Assuming that index_buffer_temp_given is NOT FULL, then call the read function
        """

        """
        Add char from File to buffer_temp, return amount of bytes written to buffer
    
        Notes:
            The read function should mimic C's read system call 
    
        """
        amount_bytes_char_buffer_temp_written_to = read(filename,
                                                        buffer_temp,
                                                        index_file_current,
                                                        index_buffer_temp_given,
                                                        1)

        amount_bytes_char_buffer_temp_written_to_total += amount_bytes_char_buffer_temp_written_to

        """
        If amount_bytes_char_buffer_temp_written_to == 0 
        then you are out of bounds implying that you are at the end of the file
        """
        # print(f"{amount_bytes_char_buffer_temp_written_to=}")
        # print(f"{buffer_temp=}")

        # If the amount of bytes written to buffer_temp is 0, then return amount_int_buffer_output_given
        if amount_bytes_char_buffer_temp_written_to == 0:

            # Buffer input to buffer output
            buffer_output[index_buffer_output_given] = int(
                "".join(buffer_temp[0:index_buffer_temp_given]))

            # Increment index for index_buffer_output_given
            index_buffer_output_given += 1

            # Increment the amount of ints in buffer_output
            amount_int_buffer_output_given += 1

            # Reset index for index_buffer_input_temp
            index_buffer_temp_given = 0

            return amount_int_buffer_output_given, amount_bytes_char_buffer_temp_written_to_total

        # Check if index_buffer_temp in buffer_temp is ","
        elif buffer_temp[index_buffer_temp_given] == DELIMITER:

            # atoi (ascii to int) operation on buffer_temp into buffer_output
            buffer_output[index_buffer_output_given] = int(
                "".join(buffer_temp[0:index_buffer_temp_given]))

            # Increment index for index_buffer_output_given
            index_buffer_output_given += 1

            # Increment the amount of ints in buffer_output
            amount_int_buffer_output_given += 1

            # Reset index for index_buffer_input_temp
            index_buffer_temp_given = 0

        else:
            index_buffer_temp_given += 1

        # If the buffer_output is full, then return amount_int_buffer_output_given
        if amount_int_buffer_output_given == buffer_output.get_size_buffer_max():
            return amount_int_buffer_output_given, amount_bytes_char_buffer_temp_written_to_total

        index_file_current += 1


def _get_bytes_from_int(int_given: int) -> int:
    """
    Fast int to char byte conversion

    Notes:
        A little cheaty... since it's not in C


    pseudocode:
        _get_bytes_from_int(int_given):
            counter = 0
            for i in str(int_given):
                counter++

            return counter

    :param int_given: int
    :return: bytes in as a char
    """
    return len(str(int_given))


def _get_bytes_from_int_buffer(buffer: Buffer,
                               amount_bytes_char_file_partition_written_to: int,
                               delimiter: Union[str, None] = None):
    """

    pseudocode:
        _get_bytes_from_int_buffer(buffer, amount_bytes_char_file_partition_written_to):
            byte_count = 0

            for int in buffer:
                byte_count += do logic to calculate bytes

            return byte_count

    :return:
    """

    amount_bytes = 0

    # Calculate bytes from amount of delimiters
    if delimiter is not None:
        amount_bytes_char_delimiter = (
                ((len(buffer) - 1) * len(delimiter) if len(buffer) > 1 else 0) +  # Buffers delimiters
                (len(delimiter) if amount_bytes_char_file_partition_written_to > 0 else 0)  # file has stuff in it
        )

        amount_bytes += amount_bytes_char_delimiter

    # Calculate bytes from buffer
    for i in buffer:
        amount_bytes += _get_bytes_from_int(i)

    return amount_bytes


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def merge_files_to_file(filename_left: str,
                        amount_bytes_filename_left: int,
                        filename_right: str,
                        amount_bytes_filename_right: int,
                        filename_base: str,
                        side: str,
                        buffer_input_left: Buffer,
                        buffer_input_right: Buffer,
                        buffer_output: Buffer,
                        _index_stack_frame: int,
                        amount_bytes_per_temp_file_max: Union[int, None] = None
                        ) -> List[Tuple[str, int]]:
    """

    MERGE FILES IN 1 FILE

    IMPORTANT NOTES:
        index_file_left AND index_file_right ASSUMES THAT
        amount_bytes_char_buffer_left == index_file_left AND
        amount_bytes_char_buffer_right == index_file_right AND
        SO DON'T USE CHARS PAST ascii FOR UTF-8

    :param filename_left:
    :param amount_bytes_filename_left:
    :param filename_right:
    :param amount_bytes_filename_right:
    :param filename_base:
    :param side:
    :param buffer_input_left:
    :param buffer_input_right:
    :param buffer_output:
    :param _index_stack_frame:
    :param amount_bytes_per_temp_file_max:
    :return:
    """
    index_file_left = 0

    index_file_right = 0

    pointer_buffer_output = 0

    pointer_buffer_input_left = 0

    pointer_buffer_input_right = 0

    amount_int_buffer_input_left = 0

    amount_int_buffer_input_right = 0

    amount_int_buffer_output = 0

    amount_bytes_char_file_partition_written_to = 0

    index_file_partition = 0  # Partition index

    list_filename_merged: List[Tuple[str, int]] = []

    filename_merged = "{}_{}_{}_{}".format(filename_base.replace(".txt", ""),
                                           "merge",
                                           _index_stack_frame,
                                           side
                                           )

    """
    READ FILE INTO INPUT BUFFER
    MERGE SORT INTO OUTPUT BUFFER
        IF INPUT BUFFER EMPTY READ FROM FILE L OR R
            REQUIRES A TEMP BUFFER (OUTPUT BUFFER)
        IF OUTPUT BUFFER FULL FLUSH TO FILE MERGED
    
    """
    while (
            ((amount_int_buffer_input_left > 0) or (amount_int_buffer_input_right > 0)) or
            ((amount_bytes_filename_left > 0) or (amount_bytes_filename_right > 0))
    ):

        # DEBUGGING
        # print("---------------------")
        # print(f"{amount_bytes_filename_left=}\n"
        #       f"{amount_bytes_filename_right=}\n"
        #       f"{amount_int_buffer_input_left=}\n"
        #       f"{amount_int_buffer_input_right=}\n"
        #       # f"{buffer_input_left[pointer_buffer_input_left]=}\n"
        #       f"{pointer_buffer_input_left=}\n"
        #       # f"{buffer_input_right[pointer_buffer_input_right]=}\n",
        #       f"{pointer_buffer_input_right=}\n"
        #       # f"{buffer_output[pointer_buffer_output]=}\n"
        #       f"{pointer_buffer_output=}\n"
        #       f"{buffer_input_left=}\n"
        #       f"{buffer_input_right=}\n"
        #       f"{buffer_output=}\n"
        #       )
        # print("---------------------")

        """ #################### REFILL ZONE #################### """

        # If there is nothing in the left buffer AND there are ints in the left file
        if amount_int_buffer_input_left == 0 and amount_bytes_filename_left > 0:
            # print("buffer_input_left is empty!")

            if amount_int_buffer_output != 0:
                # print("Flush: buffer_output is required for fill up buffer_input_left")

                filename_current_instance = "{}_{}.txt".format(filename_merged, index_file_partition)
                # filename_current_instance = _get_filename_current_instance(filename_merged, index_file_partition)

                # Flush
                amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                    filename_current_instance, buffer_output[0:pointer_buffer_output])

                # Increment amount of bytes to amount_bytes_char_file_partition_written_to
                amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

                # Reset pointer for buffer_output
                pointer_buffer_output = 0

                if filename_current_instance_returned is not None:
                    list_filename_merged.append((filename_current_instance,
                                                 amount_bytes_char_file_partition_written_to))
                else:
                    list_filename_merged[index_file_partition] = (filename_current_instance,
                                                                  amount_bytes_char_file_partition_written_to)

                # Reset amount of ints in buffer_output
                amount_int_buffer_output = 0

            amount_int_temp, amount_bytes_char_temp = fill_int_buffer(filename_left,
                                                                      buffer_input_left,
                                                                      buffer_output,
                                                                      index_file_left)

            index_file_left += amount_bytes_char_temp

            amount_int_buffer_input_left = amount_int_temp

            amount_bytes_filename_left -= amount_bytes_char_temp

            pointer_buffer_input_left = 0

        # If there is nothing in the right buffer AND there are ints in the right file
        if amount_int_buffer_input_right == 0 and amount_bytes_filename_right > 0:
            # print("buffer_input_right is empty!")

            if amount_int_buffer_output != 0:
                # print("Flush: buffer_output is required for fill up buffer_input_right")

                filename_current_instance = "{}_{}.txt".format(filename_merged, index_file_partition)
                # filename_current_instance = _get_filename_current_instance(filename_merged, index_file_partition)

                # Flush
                amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                    filename_current_instance, buffer_output[0:pointer_buffer_output])

                # Increment amount of bytes to amount_bytes_char_file_partition_written_to
                amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

                # Reset pointer for buffer_output
                pointer_buffer_output = 0

                if filename_current_instance_returned is not None:
                    list_filename_merged.append((filename_current_instance,
                                                 amount_bytes_char_file_partition_written_to))
                else:
                    list_filename_merged[index_file_partition] = (filename_current_instance,
                                                                  amount_bytes_char_file_partition_written_to)

                # Reset amount of ints in buffer_output
                amount_int_buffer_output = 0

            amount_int_temp, amount_bytes_char_temp = fill_int_buffer(filename_right,
                                                                      buffer_input_right,
                                                                      buffer_output,
                                                                      index_file_right)

            index_file_right += amount_bytes_char_temp

            amount_int_buffer_input_right = amount_int_temp

            amount_bytes_filename_right -= amount_bytes_char_temp

            pointer_buffer_input_right = 0

        """ #################### MERGING ZONE #################### """

        if (amount_int_buffer_input_left > 0) and (amount_int_buffer_input_right > 0):

            if ((buffer_input_left[pointer_buffer_input_left] <=
                 buffer_input_right[pointer_buffer_input_right])):

                # print("Merge: left size <= right size")

                buffer_output[pointer_buffer_output] = buffer_input_left[pointer_buffer_input_left]

                pointer_buffer_output += 1
                pointer_buffer_input_left += 1
                amount_int_buffer_output += 1
                amount_int_buffer_input_left -= 1

            elif (
                    (buffer_input_right[pointer_buffer_input_right] <=
                     buffer_input_left[pointer_buffer_input_left])):

                # print("Merge: right size <= left size")

                buffer_output[pointer_buffer_output] = buffer_input_right[pointer_buffer_input_right]
                pointer_buffer_output += 1
                pointer_buffer_input_right += 1
                amount_int_buffer_output += 1
                amount_int_buffer_input_right -= 1

        elif amount_int_buffer_input_left > 0:
            # print("Merge: left size still has items")

            buffer_output[pointer_buffer_output] = buffer_input_left[pointer_buffer_input_left]

            pointer_buffer_output += 1
            pointer_buffer_input_left += 1
            amount_int_buffer_output += 1
            amount_int_buffer_input_left -= 1

        elif amount_int_buffer_input_right > 0:
            # print("Merge: right size still has items")

            buffer_output[pointer_buffer_output] = buffer_input_right[pointer_buffer_input_right]

            pointer_buffer_output += 1
            pointer_buffer_input_right += 1
            amount_int_buffer_output += 1
            amount_int_buffer_input_right -= 1

        """ #################### FLUSHING ZONE #################### """

        amount_bytes_char_file_partition_delimiter = (
                ((amount_int_buffer_output - 1) * len(DELIMITER) if amount_int_buffer_output > 1 else 0) +
                (len(DELIMITER) if amount_bytes_char_file_partition_written_to > 0 else 0)
        )

        amount_bytes_char_buffers_max = (max((_get_bytes_from_int(
            buffer_input_left[pointer_buffer_input_left]) if amount_int_buffer_input_left > 0 else 0),
                                             (_get_bytes_from_int(buffer_input_right[
                                                                      pointer_buffer_input_right]) if amount_int_buffer_input_right > 0 else 0)) +
                                         (len(DELIMITER) if amount_bytes_char_file_partition_written_to > 0 else 0)
                                         )

        if (amount_bytes_per_temp_file_max is not None and
                (
                        ((amount_bytes_char_file_partition_written_to +
                          amount_bytes_char_buffers_max +
                          _get_bytes_from_int_buffer(buffer_output[0:amount_int_buffer_output],
                                                     amount_bytes_char_file_partition_written_to,
                                                     delimiter=DELIMITER) +
                          amount_bytes_char_file_partition_delimiter
                         ) >= amount_bytes_per_temp_file_max and amount_int_buffer_output != 0)
                )

        ):
            # print("Flush: limited by amount_bytes_per_temp_file_max")

            filename_current_instance = "{}_{}.txt".format(filename_merged, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_merged, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                filename_current_instance, buffer_output[0:pointer_buffer_output])

            # Increment amount of bytes to amount_bytes_char_file_partition_written_to
            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            # Reset pointer for buffer_output
            pointer_buffer_output = 0

            if filename_current_instance_returned is not None:
                list_filename_merged.append((filename_current_instance,
                                             amount_bytes_char_file_partition_written_to))
            else:
                list_filename_merged[index_file_partition] = (filename_current_instance,
                                                              amount_bytes_char_file_partition_written_to)

            # Reset amount of bytes written to file partition
            amount_bytes_char_file_partition_written_to = 0

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

            # Increment the index for the file partition
            index_file_partition += 1

        elif amount_int_buffer_output == buffer_output.get_size_buffer_max() and amount_int_buffer_output != 0:
            # print("Flush: buffer_output is full")

            filename_current_instance = "{}_{}.txt".format(filename_merged, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_merged, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                filename_current_instance, buffer_output)

            # Increment amount of bytes to amount_bytes_char_file_partition_written_to
            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            # Reset pointer for buffer_output
            pointer_buffer_output = 0

            if filename_current_instance_returned is not None:
                list_filename_merged.append((filename_current_instance,
                                             amount_bytes_char_file_partition_written_to))
            else:
                list_filename_merged[index_file_partition] = (filename_current_instance,
                                                              amount_bytes_char_file_partition_written_to)

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

        elif (amount_int_buffer_input_left == 0) and (amount_int_buffer_input_right == 0) and (
                amount_int_buffer_output != 0):
            # print("Flush: both buffers are empty")

            filename_current_instance = "{}_{}.txt".format(filename_merged, index_file_partition)
            # filename_current_instance = _get_filename_current_instance(filename_merged, index_file_partition)

            # Flush
            amount_bytes_char_file_partition_written_to_temp, filename_current_instance_returned = flush_to_file(
                filename_current_instance, buffer_output[0:pointer_buffer_output])

            # Increment amount of bytes to amount_bytes_char_file_partition_written_to
            amount_bytes_char_file_partition_written_to += amount_bytes_char_file_partition_written_to_temp

            # Reset pointer for buffer_output
            pointer_buffer_output = 0

            if filename_current_instance_returned is not None:
                list_filename_merged.append((filename_current_instance,
                                             amount_bytes_char_file_partition_written_to))
            else:
                list_filename_merged[index_file_partition] = (filename_current_instance,
                                                              amount_bytes_char_file_partition_written_to)

            # Reset amount of ints in buffer_output
            amount_int_buffer_output = 0

        # DEBUGGING
        # print("---------------------")
        # print(f"{amount_bytes_filename_left=}\n"
        #       f"{amount_bytes_filename_right=}\n"
        #       f"{amount_int_buffer_input_left=}\n"
        #       f"{amount_int_buffer_input_right=}\n"
        #       f"{amount_bytes_char_file_partition_written_to=}\n"
        #       # f"{buffer_input_left[pointer_buffer_input_left]=}\n"
        #       f"{pointer_buffer_input_left=}\n"
        #       # f"{buffer_input_right[pointer_buffer_input_right]=}\n",
        #       f"{pointer_buffer_input_right=}\n"
        #       # f"{buffer_output[pointer_buffer_output]=}\n"
        #       f"{pointer_buffer_output=}\n"
        #       f"{buffer_input_left=}\n"
        #       f"{buffer_input_right=}\n"
        #       f"{buffer_output=}\n"
        #       )
        # print("---------------------")
        # print("END")

    # Delete the files that made the merged file
    # print(f"{merge_sort_buffered.__name__} Deleting:",filename_left)
    # print(f"{merge_sort_buffered.__name__} Deleting:",filename_right)
    del DIRECTORY_CURRENT_WORKING[filename_left]
    del DIRECTORY_CURRENT_WORKING[filename_right]

    return list_filename_merged


# @algorithm_recorder.decorator_wrapper_callable
# @_debugging_decorator
# @callgraph
def merge_sort_buffered(list_tuple_filename_bytes: List[Tuple[str, int]],
                        filename_base: str,
                        _index_stack_frame: int = None,
                        _side: str = None) -> List[Union[Tuple[str, int], str]]:
    """
    Modified merge sort using a buffer

    :param list_tuple_filename_bytes: [(filename, bytes)]
    :param filename_base: base_filename
    :param _index_stack_frame: stack index frame
    :param _side: left or Right side
    :return: [(filename, bytes)], base_filename
    """
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    # Default value initializer
    if _index_stack_frame is None:
        _index_stack_frame = 0  # stack frame index

    # Print the directory
    # for k, v in DIRECTORY_CURRENT_WORKING.items():
    #     print(k, v)
    # print()

    # Number of ints in the file
    number_of_ints_in_file = get_amount_int_in_file(list_tuple_filename_bytes[0][0], BUFFER_INPUT_LEFT)

    """ #################### Base Case #################### """
    # If number of ints in files == 1
    if number_of_ints_in_file == 1:
        # print("File size is 1 byte")

        return list_tuple_filename_bytes

    """ #################### Split file #################### """
    list_tuple_base_left, list_tuple_base_right = split_file_to_files(list_tuple_filename_bytes[0][0],
                                                                      filename_base,
                                                                      BUFFER_OUTPUT,
                                                                      BUFFER_INPUT_LEFT,
                                                                      _index_stack_frame=_index_stack_frame + 1)

    # print("After split_file_to_files")
    # print(list_tuple_base_left)
    # print()
    # print(list_tuple_base_right)
    # print()

    list_tuple_base_left_new = merge_sort_buffered(list_tuple_base_left,
                                                   filename_base,
                                                   _index_stack_frame + 1,
                                                   _side="L")

    list_tuple_base_right_new = merge_sort_buffered(list_tuple_base_right,
                                                    filename_base,
                                                    _index_stack_frame + 1,
                                                    _side="R")

    # print("After both merge_sort_buffered")
    # print(list_tuple_base_left_new)
    # print(DIRECTORY_CURRENT_WORKING[list_tuple_base_left_new[0][0]])
    # print()
    # print(list_)
    # print(DIRECTORY_CURRENT_WORKING[list_[0][0]])
    # print()

    """ #################### 2 way Merge #################### """
    list_filename_merged_new = merge_files_to_file(list_tuple_base_left_new[0][0],
                                                   list_tuple_base_left_new[0][1],
                                                   list_tuple_base_right_new[0][0],
                                                   list_tuple_base_right_new[0][1],
                                                   filename_base,
                                                   _side,
                                                   BUFFER_INPUT_LEFT,
                                                   BUFFER_INPUT_RIGHT,
                                                   BUFFER_OUTPUT,
                                                   _index_stack_frame)

    return list_filename_merged_new


def _test_read():
    DIRECTORY_CURRENT_WORKING["test"] = "123456"

    buffer_test = Buffer("buffer_test", 10)

    read("test", buffer_test, 1, 3, 3)

    print(buffer_test)


def _test_write():
    DIRECTORY_CURRENT_WORKING["test"] = "123456"

    buffer_test = Buffer("buffer_test", 10)

    for i, e in enumerate(buffer_test):
        buffer_test[i] = i

    write("test", buffer_test)
    write("test", buffer_test, append=True)

    print(DIRECTORY_CURRENT_WORKING["test"])


def _test_split_file_to_files():
    DIRECTORY_CURRENT_WORKING["test.txt"] = "1,2,3,45,6,19,23,1,442,5,102,4,1"

    DIRECTORY_CURRENT_WORKING["test.txt"] = "3,5,9,2,6,1,6,7,23"
    DIRECTORY_CURRENT_WORKING["test.txt"] = "3,5,9,2,6,1,6,7,9"

    # buffer_split_dude("test.txt", amount_bytes_per_temp_file_max=3)
    list_filename_left, list_filename_right = split_file_to_files("test.txt", "test.txt",
                                                                  BUFFER_OUTPUT,
                                                                  BUFFER_INPUT_LEFT,
                                                                  amount_bytes_per_temp_file_max=None)

    print("list_filename_left")
    for i in list_filename_left:
        print(i)
    print()

    print("list_filename_right")
    for i in list_filename_right:
        print(i)
    print()

    for k, v in DIRECTORY_CURRENT_WORKING.items():
        print("\t", k, "\t", v)


def _test_fill_int_buffer():
    DIRECTORY_CURRENT_WORKING["test.txt"] = "3,5,9,2,6,1,6,7,23"

    print(fill_int_buffer("test.txt", BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, 14))
    print(BUFFER_INPUT_LEFT)


def _test_merge_files_to_file():
    global DIRECTORY_CURRENT_WORKING

    DIRECTORY_CURRENT_WORKING["test_1.txt"] = "3,5,9,100,101"
    DIRECTORY_CURRENT_WORKING["test_2.txt"] = "2,4,5,34,99,100"

    merge_files_to_file("test_1.txt", len(DIRECTORY_CURRENT_WORKING["test_1.txt"]),
                        "test_2.txt", len(DIRECTORY_CURRENT_WORKING["test_2.txt"]),
                        "test.txt", "L",
                        BUFFER_INPUT_LEFT,
                        BUFFER_INPUT_RIGHT,
                        BUFFER_OUTPUT, 0, amount_bytes_per_temp_file_max=3)

    for k, v in DIRECTORY_CURRENT_WORKING.items():
        print("\t", k, "\t", v)
    print()

    # RESET THE DIRECTORY
    DIRECTORY_CURRENT_WORKING = {}

    DIRECTORY_CURRENT_WORKING["test_1.txt"] = "3"
    DIRECTORY_CURRENT_WORKING["test_2.txt"] = "2"

    merge_files_to_file("test_1.txt", len(DIRECTORY_CURRENT_WORKING["test_1.txt"]),
                        "test_2.txt", len(DIRECTORY_CURRENT_WORKING["test_2.txt"]),
                        "test.txt", "L",
                        BUFFER_INPUT_LEFT,
                        BUFFER_INPUT_RIGHT,
                        BUFFER_OUTPUT, 0)

    for k, v in DIRECTORY_CURRENT_WORKING.items():
        print("\t", k, "\t", v)
    print()


def print_algo_info():
    print()
    print("Algorithm Info:")
    print(f"Amount of {flush_to_file.__name__} calls: {_counter_flush_to_file}")
    print(f"Amount of {read.__name__} calls: {_counter_read}")
    print(f"Amount of {write.__name__} calls: {_counter_write}")

    print()
    print("{}{:<30}{}".format(4 * " ", "File:", "Content:"))
    print_directory()


def print_directory():
    for k, v in DIRECTORY_CURRENT_WORKING.items():
        print("{}{:<30}{}".format(4 * " ", k, v))
    print()


def reset_global_vars():
    global DELIMITER, BUFFER_SIZE_OUTPUT, BUFFER_SIZE_INPUT, DIRECTORY_CURRENT_WORKING
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT
    global _counter_write, _counter_read, _counter_flush_to_file
    global _id_unique

    DELIMITER = ","
    BUFFER_SIZE_INPUT = 4096
    BUFFER_SIZE_OUTPUT = 4096
    DIRECTORY_CURRENT_WORKING = {}

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)

    _id_unique = 0
    _counter_flush_to_file = 0
    _counter_read = 0
    _counter_write = 0


@_debugging_decorator(debug_vars=False)
def _example_small():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", 4)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", 4)
    BUFFER_OUTPUT = Buffer("Buffer output", 4)
    print()

    DIRECTORY_CURRENT_WORKING["text.txt"] = "3,5,9,2,6,1,6,7,23,2,1,65,7,2,4,5,32,65,17,7,92,54"  # 50 bytes
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_small_32_ints():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)
    print()

    # 72 bytes
    DIRECTORY_CURRENT_WORKING["text.txt"] = "3,5,9,2,6,1,6,7,23,2,1,65,7,2,4,5,32,65,17,7,92,54,32,12,54,2,3,1,12,2,6,7"
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_small_16_ints():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)
    print()

    DIRECTORY_CURRENT_WORKING["text.txt"] = "3,5,9,2,6,1,6,7,23,2,1,65,7,2,4,5"  # 33 bytes
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_small_8_ints():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)
    print()

    DIRECTORY_CURRENT_WORKING["text.txt"] = "3,5,9,2,6,1,6,7"  # 15 bytes
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_small_3_digits():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", 4)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", 4)
    BUFFER_OUTPUT = Buffer("Buffer output", 4)
    print()

    DIRECTORY_CURRENT_WORKING[
        "text.txt"] = "300,500,900,200,600,100,600,700,230,200,100,650,700,200,400,500,320,650,170,700,920,540"
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_challenge_small():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)
    print()

    DIRECTORY_CURRENT_WORKING["text.txt"] = "3,5,9,2,6,1,6,7,23,2,1,65,7,2,4,5,32,65,17,7,92,54"  # 50 bytes
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_challenge_bigger():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", BUFFER_SIZE_INPUT)
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", BUFFER_SIZE_INPUT)
    BUFFER_OUTPUT = Buffer("Buffer output", BUFFER_SIZE_OUTPUT)
    print()

    DIRECTORY_CURRENT_WORKING[
        "text.txt"] = "31123,524,9543,2123,665,176,236,567,23,1232,651,65,767,2,874,5,312,365,1437,127,392,554"
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    print_algo_info()
    reset_global_vars()


@_debugging_decorator(debug_vars=False)
def _example_challenge_32_bytes():
    global BUFFER_INPUT_LEFT, BUFFER_INPUT_RIGHT, BUFFER_OUTPUT

    BUFFER_INPUT_LEFT = Buffer("Buffer input left", 4096)  # 4096 bytes
    BUFFER_INPUT_RIGHT = Buffer("Buffer input right", 4096)  # 4096 bytes
    BUFFER_OUTPUT = Buffer("Buffer output", 4096)  # 4096 bytes
    print()

    """
    DIRECTORY_CURRENT_WORKING mimics a Directory on your computer
    text.txt is the file name
    "6,23,999,15,2,73,9,56,23,7,12,44" is 32 bytes (32 chars long)
    
    """
    DIRECTORY_CURRENT_WORKING["text.txt"] = "6,23,999,15,2,73,9,56,23,7,12,44"  # 32 bytes
    bytes_file = len(DIRECTORY_CURRENT_WORKING["text.txt"])  # Calculate bytes in "text.txt"

    # Run algorithm
    result = merge_sort_buffered([("text.txt", bytes_file)], "text.txt")

    # Prints the files in the directory
    print_algo_info()

    # Reset vars for a new run
    reset_global_vars()


if __name__ == '__main__':
    # _example_small()
    _example_small_8_ints()
    _example_small_16_ints()
    _example_small_32_ints()
    # _example_small_3_digits()
    # _example_challenge_small()
    # _example_challenge_bigger()
    # _example_challenge_32_bytes()

    # _test_read()
    # _test_write()
    # _test_fill_buffer_int()
    # _test_split_file_to_files()
    # _test_merge_files_to_file()

    # Custom stuff
    # create_callgraph()
    # algorithm_recorder.print()
    pass
