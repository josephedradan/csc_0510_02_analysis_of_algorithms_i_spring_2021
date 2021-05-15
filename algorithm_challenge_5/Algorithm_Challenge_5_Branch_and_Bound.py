"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 5/9/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:
    7.3 Traveling Salesman Problem - Branch and Bound
        https://www.youtube.com/watch?v=1FEP_sNb62k

    Travelling Salesman Problem using Branch and Bound
        https://www.youtube.com/watch?v=HjSbaKF8Gi0
"""
from __future__ import annotations

import heapq
import numpy
from functools import wraps
from typing import List, Tuple, Union, Sequence

dict_k_callable_v_amount_call = {}


def decorator_callable_count(callable_given: Union[callable, None] = None,
                             dict_k_callable_v_amount_call_given: dict = None):
    """
    Simple high level callable counter decorator

    :param callable_given:
    :param dict_k_callable_v_amount_call_given:
    :return:
    """

    def decorator_callable_count_actual(callable_given):
        @wraps(callable_given)
        def decorator_callable_wrapper(*args, **kwargs):
            if dict_k_callable_v_amount_call_given.get(callable_given.__name__) is None:
                dict_k_callable_v_amount_call_given[callable_given.__name__] = 0

            dict_k_callable_v_amount_call_given[callable_given.__name__] += 1

            result = callable_given(*args, **kwargs)
            return result

        return decorator_callable_wrapper

    return decorator_callable_count_actual(callable_given) if callable_given else decorator_callable_count_actual


class SolutionContainerSingle:
    def __init__(self,
                 given: Union[int, SolutionContainerSingle] = None):

        if isinstance(given, int):
            index_node_start = given

            ###
            self.index_node_start: Union[int] = index_node_start
            self.exit_sum_cost_path_complete = 0
            self.exit_index_node_parent: Union[int] = index_node_start
            self.exit_list_node_path: Union[List[int]] = [index_node_start]
            self.exit_sum_cost_path_direct_full = 0

        elif isinstance(given, SolutionContainerSingle):
            """
            Remember to call 
                set_exit_sum_cost_path_complete
                set_exit_index_node_parent
                set_exit_sum_cost_path_direct_full

                set_entry_sum_cost_path
                set_entry_index_node_child
                set_entry_sum_cost_path_direct_full

            """
            solution_container_single = given
            ###
            self.index_node_start: Union[int] = solution_container_single.get_index_node_start()
            self.exit_sum_cost_path_complete: Union[int] = 0
            self.exit_index_node_parent: Union[int] = 0
            self.exit_list_node_path: Union[List[int]] = solution_container_single.get_list_node_path().copy()
            self.exit_sum_cost_path_direct_full: Union[int] = 0

    def get_sum_cost_path_complete(self) -> int:
        return self.exit_sum_cost_path_complete

    def set_sum_cost_path_complete(self, value: int):
        self.exit_sum_cost_path_complete = value

    def get_index_node_start(self) -> int:
        return self.index_node_start

    def add_to_list_node_path(self, index_node: int):
        self.exit_list_node_path.append(index_node)

    def get_list_node_path(self) -> List:
        return self.exit_list_node_path

    def get_sum_cost_path_direct_full(self) -> int:
        return self.exit_sum_cost_path_direct_full

    def set_sum_cost_path_direct_full(self, value: int):
        self.exit_sum_cost_path_direct_full = value

    def get_index_node_parent(self) -> int:
        return self.exit_index_node_parent

    def set_index_node_parent(self, index_node_parent: int):
        self.exit_index_node_parent = index_node_parent

    def __str__(self):
        return "({}, {})".format(self.get_sum_cost_path_complete(),
                                 self.exit_list_node_path)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, path_solution: SolutionContainer):
        return self.get_sum_cost_path_complete() < path_solution.get_sum_cost_path_complete()


class SolutionContainer:
    def __init__(self,
                 given: Union[int, SolutionContainer] = None):

        if isinstance(given, int):
            index_node_start = given

            ###
            self.index_node_start: Union[int] = index_node_start
            # self.sum_cost_path_direct: Union[int] = 0

            ###

            self.exit_sum_cost_path_complete = 0
            self.exit_index_node_parent: Union[int] = index_node_start
            self.exit_list_node_path: Union[List[int]] = [index_node_start]
            self.exit_sum_cost_path_direct_full = 0

            ###
            self.entry_sum_cost_path_complete = 0
            self.entry_index_node_child: Union[int] = index_node_start
            self.entry_list_node_path: Union[List[int]] = [index_node_start]
            self.entry_sum_cost_path_direct_full = 0

        elif isinstance(given, SolutionContainer):
            """
            Remember to call 
                set_exit_sum_cost_path_complete
                set_exit_index_node_parent
                set_exit_sum_cost_path_direct_full
                
                set_entry_sum_cost_path
                set_entry_index_node_child
                set_entry_sum_cost_path_direct_full
                
            """
            solution_container = given
            ###
            self.index_node_start: Union[int] = solution_container.get_index_node_start()
            ###

            self.exit_sum_cost_path_complete: Union[int] = 0
            self.exit_index_node_parent: Union[int] = 0
            self.exit_list_node_path: Union[List[int]] = solution_container.get_exit_list_node_path().copy()
            self.exit_sum_cost_path_direct_full: Union[int] = 0

            ###
            self.entry_sum_cost_path_complete: Union[int] = 0
            self.entry_index_node_child: Union[int] = 0
            self.entry_list_node_path: Union[List[int]] = solution_container.get_entry_list_node_path().copy()
            self.entry_sum_cost_path_direct_full: Union[int] = 0

    def get_sum_cost_path_complete(self) -> int:
        return self.exit_sum_cost_path_complete + self.entry_sum_cost_path_complete
        # return self.exit_sum_cost_path_complete

    def get_index_node_start(self) -> int:
        return self.index_node_start

    ####
    def add_to_exit_list_node_path(self, index_node: int):
        self.exit_list_node_path.append(index_node)

    def get_exit_list_node_path(self) -> List:
        return self.exit_list_node_path

    def get_exit_sum_cost_path_complete(self):
        return self.exit_sum_cost_path_complete

    def set_exit_sum_cost_path_complete(self, value: int):
        self.exit_sum_cost_path_complete = value

    def get_exit_sum_cost_path_direct_full(self) -> int:
        return self.exit_sum_cost_path_direct_full

    def set_exit_sum_cost_path_direct_full(self, value: int):
        self.exit_sum_cost_path_direct_full = value

    def get_exit_index_node_parent(self) -> int:
        return self.exit_index_node_parent

    def set_exit_index_node_parent(self, index_node_parent: int):
        self.exit_index_node_parent = index_node_parent

    ####

    def add_to_entry_list_node_path(self, index_node: int):
        self.entry_list_node_path.append(index_node)

    def get_entry_list_node_path(self) -> List:
        return self.entry_list_node_path

    def get_entry_sum_cost_path_complete(self):
        return self.entry_sum_cost_path_complete

    def set_entry_sum_cost_path_complete(self, value: int):
        self.entry_sum_cost_path_complete = value

    def get_entry_sum_cost_path_direct_full(self) -> int:
        return self.entry_sum_cost_path_direct_full

    def set_entry_sum_cost_path_direct_full(self, value: int):
        self.entry_sum_cost_path_direct_full = value

    def get_entry_index_node_child(self) -> int:
        return self.entry_index_node_child

    def set_entry_index_node_child(self, index_node_child: int):
        self.entry_index_node_child = index_node_child

    # def set_standard_entry(self, index_node, value):
    #     self.add_to_entry_list_node_path(index_node)
    #     self.set_entry_index_node_child(index_node)
    #     self.set_entry_sum_cost_path_direct_full(value)

    def __str__(self):
        return "({}, {}, {})".format(self.get_sum_cost_path_complete(),
                                     self.exit_list_node_path,
                                     self.entry_list_node_path)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, path_solution: SolutionContainer):
        v1 = ((self.get_sum_cost_path_complete(),
               self.exit_index_node_parent,
               self.entry_index_node_child) <
              (path_solution.get_sum_cost_path_complete(),
               path_solution.exit_index_node_parent,
               path_solution.entry_index_node_child))
        v2 = (self.get_sum_cost_path_complete()) < path_solution.get_sum_cost_path_complete()
        return v2


# def solve_exit_node_first_dynamic_programming(matrix: Sequence[Sequence]):
#     pass

@decorator_callable_count(dict_k_callable_v_amount_call_given=dict_k_callable_v_amount_call)
def branch_and_bound_node_exit(matrix,
                               heap_queue_priority: List[Tuple[int, int, List[int], int]],
                               solution_container_current: SolutionContainer
                               ) -> int:
    """
    Notes:
        * index_node is just another way of saying node..

        Node Start:     The Node Starting (index_node_start) of the entire traversal, it is basically the Root Node
                        (e.g. A -> B). There is only 1 Node Starting and that Node is also a Node Parent.

        Node Parent:    The Node Starting (index_node_parent) that will travel to a Node Selected (e.g. B -> C ).
                        There is only 1 Node Parent that is also a Node Starting, but there can be many Node Parents.

        Node Selected:  The Node that the Node Parent connects to (e.g. C from the example of B -> C).

        Node Potential: A Node that follow this format: NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        Node Possible:  A Node that is inside the set for a Node Potential.

    :param matrix: Matrix
    :param heap_queue_priority: The Priority Queue
    :param solution_container_current:
    :return:
    """
    """
    set_index_node_traveled_to has the set of nodes used in the traversal except for the Node Starting unless the
    last node to add is the Node Starting.
    
    We require a copy of set_index_node_traveled_to as set_index_node_traveled_to_previous because 
    set_index_node_traveled_to will be modified to include a Node Selected. 
    
    set_index_node_traveled_to will be used to prevent a Node in set_index_node_traveled_to from becoming a
    Node Possible. Basically, prevent a Node Possible from being inside of set in a
    NODE_POTENTIAL -> {NODE_POSSIBLE, ...}
    
    set_index_node_traveled_to_previous will be used to prevent a Node from set_index_node_traveled_to_previous from
    becoming a Node Potential. 
    
    Example:
        set_index_node_traveled_to = {C, D}     # C and D will not be a NODE_POSSIBLE in the set in the format:
                                                # NODE_POTENTIAL -> {NODE_POSSIBLE, ...}
                                                
        set_index_node_traveled_to_previous = {D}  # D Will not be a NODE_POTENTIAL
        A -> D -> C = 10
        C -> {B} = 3
        B -> {A} = 2
    
    """
    set_index_node_traveled_to = set(solution_container_current.get_exit_list_node_path()[1:])

    set_index_node_traveled_to_previous = set_index_node_traveled_to.copy()

    for index_row_node_selected, row_main in enumerate(matrix):

        """
        Skip the Node Selected if the Node Selected is the Node Parent (Prevent calculations to self).
        
        IMPORTANT NOTE:
            THIS WILL PREVENT index_row_node_selected FROM BEING REMOVED FROM THE set_index_node_traveled_to
            EVEN THOUGH index_row_node_selected IS ALREADY IN set_index_node_traveled_to
        """
        if index_row_node_selected == solution_container_current.get_exit_index_node_parent():
            continue

        """
        Skip the Node Selected if the Node Selected has already been traveled to.

        IMPORTANT NOTE:
            THIS WILL PREVENT index_row_node_selected FROM BEING REMOVED FROM THE set_index_node_traveled_to
            EVEN THOUGH index_row_node_selected IS ALREADY IN set_index_node_traveled_to        
        """
        if index_row_node_selected in set_index_node_traveled_to:
            continue

        """
        Skip the Node Selected if the Node Selected is the Node Start (Can't jump to yourself until the end).
        Note that the Node Start is NOT added to index_row_node_selected to make the algorithm easier to use.
        """
        if (index_row_node_selected == solution_container_current.get_index_node_start() and
                len(solution_container_current.get_exit_list_node_path()) < len(matrix)):
            # print("Not the ending")
            continue

        # Initialized sum
        sum_value_min_plus_sum_cost_path_direct_full = 0

        """
        Get the Cost of a Full Direct Path
        Example:
            Cost of the Previous Sum Path Direct
              4
            A -> D
            
            Cost of the New Sum Path Direct
              6
            D -> C
            
            Cost of the Full Sum Path Direct
              4    6
            A -> D -> C
            
        """
        sum_cost_path_direct_parent_selected = matrix[solution_container_current.get_exit_index_node_parent()][
            index_row_node_selected]

        sum_cost_path_direct_full_new = sum_cost_path_direct_parent_selected + solution_container_current.get_exit_sum_cost_path_direct_full()
        # A Sum of the Sum of the Minimum Value Sum of rows + Sum of the Full Direct Path
        sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full_new

        print("Node Parent {} -> Node Selected {}: {}".format(solution_container_current.get_exit_index_node_parent(),
                                                              index_row_node_selected,
                                                              sum_value_min_plus_sum_cost_path_direct_full))

        # Add Node Selected to set of Nodes traveled to (AKA Set of Nodes Excluded)
        set_index_node_traveled_to.add(index_row_node_selected)

        print("set_index_node_traveled_to", set_index_node_traveled_to)
        print("set_index_node_traveled_to_previous", set_index_node_traveled_to_previous)

        """
        It's not possible to make Node Potential when every node has been traversed through except for the last node.
        If you assume that the dimensions of the matrix are the same, then you can say that the the size of the matrix
        represents the nodes traversed.

        Basically, you have traversed to every node, so you don't need to loop through the matrix and all you
        really need to do is add list_node_path to the path and you have traveled to every node and have gone
        back to the Node Starting.
        """
        if len(set_index_node_traveled_to) == len(matrix):
            print("It's Not possible to make Node Potentials")

            solution_container_new = SolutionContainer(solution_container_current)
            solution_container_new.set_exit_sum_cost_path_complete(sum_value_min_plus_sum_cost_path_direct_full)
            solution_container_new.set_exit_index_node_parent(index_row_node_selected)
            solution_container_new.add_to_exit_list_node_path(index_row_node_selected)

            # Add Solution Container New to priority queue.
            heapq.heappush(heap_queue_priority, solution_container_new)

            """
            Return the newly created Upper. Uppers are only made when a path has traversed all nodes and has returned 
            to the Node Starting.
            """
            return sum_value_min_plus_sum_cost_path_direct_full

        # Loop through rows in the matrix
        for index_row_node_potential, row in enumerate(matrix):

            """
            Create Node Potentials if they haven't been traversed to. Excludes the Node Selected by using
            set_index_node_traveled_to_previous
            """
            if index_row_node_potential in set_index_node_traveled_to_previous:
                continue

            """
            Skip Finding the Min for the Node Potential if the Node Potential is the Node Parent.
            Node Selected == Node Potential == Node Parent. The value added to 
            sum_value_min_plus_sum_cost_path_direct_full is added directly and not by finding the min value in the row.
            
            Basically don't find the cost to yourself. Though if the matrix didn't have 0s on the diagonal, you can
            remove this condition
            """
            if index_row_node_potential == solution_container_current.get_exit_index_node_parent():
                # Alternative to matrix[index_node_parent][index_row_node_selected] is the below:
                # sum_cost_path_direct_full_new = matrix[index_row_node_potential][index_row_node_selected]
                # sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full_new
                continue

            """
            Basically, If index_row_node_potential is the Node Starting, but the index_row_node_potential is not the
            last node to traverse to (last node to traverse to is yourself), then index_row_node_potential is not a 
            Node Potential.
            """
            if (index_row_node_potential == solution_container_current.get_index_node_start() and
                    len(solution_container_current.get_exit_list_node_path()) < len(matrix)):
                print("index_row_node_potential is index_node_start, but is not the Last Node to yourself")
                continue

            print("\tNode Potential {}".format(index_row_node_potential))

            # Current minimum Value (If the code crashes because of this, then my algorithm has a bug)
            value_min = None

            # Traverse through current row to select the Min in the row
            for index_column_node_possible, value_column in enumerate(row):

                # Skip index_column_node_possible if in set_index_node_traveled_to
                if index_column_node_possible in set_index_node_traveled_to:
                    continue

                """
                Special condition for when index_row_node_selected == index_row_node_potential. This condition is to
                prevent index_row_node_potential from connecting back to what is connecting to it.
                """
                if index_row_node_potential == index_row_node_selected:
                    """
                    The body of the following condition should only run when the Node Potentials, other than the Node
                    Selected, have exhausted their Node Possibles. If there are no Node Possibles for the Node
                    Potentials that does not include the Node Selected, then the Node Potential that is also the
                    Node Selected is allowed to make the last connection to the last Node Possible which should be
                    Node Starting.
                    """
                    if len(solution_container_current.get_exit_list_node_path()) < (len(matrix) - 1):
                        """
                        Check if index_node_parent is index_column_node_possible, if this condition is true, then
                        index_row_node_selected should not calculate the distance for index_column_node_possible. If
                        the calculation from index_row_node_potential to index_column_node_possible is allowed, then
                        it's possible for index_column_node_possible to connect back to its parent which should be
                        index_row_node_potential.
                        Example:
                            A -> B = 3
                            B -> {C, D, A} = 1  # You don't want B to connect back to A because A already points to B
                            C -> {A, D} = 5
                            D -> {A, C} = 6
                        """
                        if index_column_node_possible == solution_container_current.get_index_node_start():
                            continue

                # Skip column if the column is on the Diagonal, Comment this out if Diagonals matter.
                if index_column_node_possible == index_row_node_potential:
                    continue

                # Initialized value_min if there wasn't one to begin with
                if value_min is None:
                    value_min = value_column

                # Select new value_min in current row
                elif value_column < value_min:
                    value_min = value_column

                print("\t\t-> Node Possible {} with Value {}".format(index_column_node_possible, value_column))

            sum_value_min_plus_sum_cost_path_direct_full += value_min
            print("\tMinimum Value in row:", value_min)

        print("Sum of Minimum values + Cost of path direct full: {}\n".format(
            sum_value_min_plus_sum_cost_path_direct_full))

        solution_container_new = SolutionContainer(solution_container_current)
        solution_container_new.set_exit_sum_cost_path_complete(sum_value_min_plus_sum_cost_path_direct_full)
        solution_container_new.set_exit_index_node_parent(index_row_node_selected)
        solution_container_new.set_exit_sum_cost_path_direct_full(sum_cost_path_direct_full_new)
        solution_container_new.add_to_exit_list_node_path(index_row_node_selected)

        # Add Solution Container to the Priority Queue.
        heapq.heappush(heap_queue_priority, solution_container_new)
        # print(heap_queue_priority)

        # set_index_node_traveled_to.pop()  # Implicit removal of index_row_node_selected
        set_index_node_traveled_to.remove(index_row_node_selected)  # Explicit removal of index_row_node_selected

    """
    Returning -1 implies that an Upper has been created. Uppers are only made when a path has traversed all nodes 
    and has returned to the Node Starting.
    """
    return -1


@decorator_callable_count(dict_k_callable_v_amount_call_given=dict_k_callable_v_amount_call)
def branch_and_bound_node_entry(matrix,
                                heap_queue_priority: List[Tuple[int, int, List[int], int]],
                                solution_container_current: SolutionContainer
                                ) -> int:
    """
    Notes:
        * index_node is just another way of saying node..

        Node Start:     The Node Starting (index_node_start) of the entire traversal, it is basically the Root Node
                        (e.g. A -> B). There is only 1 Node Starting and that Node is also a Node Child.

        Node Child:     The Node Starting (index_node_child) that will travel to a Node Selected (e.g. B -> C ).
                        There is only 1 Node Child that is also a Node Starting, but there can be many Node Childs.

        Node Selected:  The Node that the Node Child connects to (e.g. C from the example of B -> C).

        Node Potential: A Node that follow this format: NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        Node Possible:  A Node that is inside the set for a Node Potential.

    :param matrix: Matrix
    :param heap_queue_priority: The Priority Queue
    :param solution_container_current:
    :return:
    """
    """
    set_index_node_traveled_to has the set of nodes used in the traversal except for the Node Starting unless the
    last node to add is the Node Starting.

    We require a copy of set_index_node_traveled_to as set_index_node_traveled_to_previous because 
    set_index_node_traveled_to will be modified to include a Node Selected. 

    set_index_node_traveled_to will be used to prevent a Node in set_index_node_traveled_to from becoming a
    Node Possible. Basically, prevent a Node Possible from being inside of set in a
    NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

    set_index_node_traveled_to_previous will be used to prevent a Node from set_index_node_traveled_to_previous from
    becoming a Node Potential. 
    
    Example:
        set_index_node_traveled_to = {A, B}     # A and B will not be a NODE_POSSIBLE in the set in the format:
                                                # NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        set_index_node_traveled_to_previous = {B}  # B Will not be a NODE_POTENTIAL
        Node Selected = C   # C Will not be a NODE_POTENTIAL
        
        A <- D <- C = 5
        D -> {C} = 6
        A -> {D} = 4

    """
    set_index_node_traveled_to = set(solution_container_current.get_entry_list_node_path()[1:])

    set_index_node_traveled_to_previous = set_index_node_traveled_to.copy()

    for index_row_node_selected, row_main in enumerate(matrix):

        """
        Skip the Node Selected if the Node Selected is the Node Parent (Prevent calculations to self).

        IMPORTANT NOTE:
            THIS WILL PREVENT index_row_node_selected FROM BEING REMOVED FROM THE set_index_node_traveled_to
            EVEN THOUGH index_row_node_selected IS ALREADY IN set_index_node_traveled_to
        """
        if index_row_node_selected == solution_container_current.get_entry_index_node_child():
            continue

        """
        Skip the Node Selected if the Node Selected has already been traveled to.

        IMPORTANT NOTE:
            THIS WILL PREVENT index_row_node_selected FROM BEING REMOVED FROM THE set_index_node_traveled_to
            EVEN THOUGH index_row_node_selected IS ALREADY IN set_index_node_traveled_to        
        """
        if index_row_node_selected in set_index_node_traveled_to:
            continue

        """
        Skip the Node Selected if the Node Selected is the Node Start (Can't jump to yourself until the end).
        Note that the Node Start is NOT added to index_row_node_selected to make the algorithm easier to use.
        """
        if (index_row_node_selected == solution_container_current.get_index_node_start() and
                len(solution_container_current.get_entry_list_node_path()) < len(matrix)):
            # print("Not the ending")
            continue

        # Initialized sum
        sum_value_min_plus_sum_cost_path_direct_full = 0

        """
        Get the Cost of a Full Direct Path
        Example:
            Cost of the Previous Sum Path Direct
              2
            A <- B

            Cost of the New Sum Path Direct
              3
            B <- C

            Cost of the Full Sum Path Direct
              2    3
            A <- b <- C

        """

        # (Code Difference) The Positions of index_row_node_selected and index_node_child are swapped
        sum_cost_path_direct_selected_child = matrix[index_row_node_selected][
            solution_container_current.get_entry_index_node_child()]

        sum_cost_path_direct_full_new = (sum_cost_path_direct_selected_child +
                                         solution_container_current.get_entry_sum_cost_path_direct_full())

        # A Sum of the Sum of the Minimum Value Sum of rows + Sum of the Full Direct Path
        sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full_new

        print("Node Selected {} -> Node Child {}: {}".format(index_row_node_selected,
                                                             solution_container_current.get_entry_index_node_child(),
                                                             sum_value_min_plus_sum_cost_path_direct_full))

        """
        Add Node Child to set of Nodes traveled to (AKA Set of Nodes Excluded)
        (Code Difference) index_node_child replaces index_row_node_selected
        """
        set_index_node_traveled_to.add(solution_container_current.get_entry_index_node_child())

        # (Code Difference) index_node_start needs to be added to set_index_node_traveled_to
        set_index_node_traveled_to.add(solution_container_current.get_index_node_start())

        print("set_index_node_traveled_to", set_index_node_traveled_to)
        print("set_index_node_traveled_to_previous", set_index_node_traveled_to_previous)

        """
        It's not possible to make Node Potential when every node has been traversed through except for the last node.
        If you assume that the dimensions of the matrix are the same, then you can say that the the size of the matrix
        represents the nodes traversed.

        Basically, you have traversed to every node, so you don't need to loop through the matrix and all you
        really need to do is add list_node_path to the path and you have traveled to every node and have gone
        back to the Node Starting.
        """
        if len(set_index_node_traveled_to) == len(matrix):
            print("It's Not possible to make Node Potentials")

            solution_container_new = SolutionContainer(solution_container_current)
            solution_container_new.set_entry_sum_cost_path_complete(sum_value_min_plus_sum_cost_path_direct_full)
            solution_container_new.set_entry_index_node_child(index_row_node_selected)
            solution_container_new.add_to_entry_list_node_path(index_row_node_selected)

            # Add Solution Container New to priority queue.
            heapq.heappush(heap_queue_priority, solution_container_new)

            """
            Return the newly created Upper. Uppers are only made when a path has traversed all nodes and has returned 
            to the Node Starting.
            """
            return sum_value_min_plus_sum_cost_path_direct_full

        """
        Loop through rows in the matrix
        (Code Difference) This loop is now ranged based and now uses pseudo indices
        (THIS WILL CRASH IF MATRIX DOES NOT HAVE THE SAME DIMENSION)
        """
        for index_pseudo_column_node_potential in range(len(matrix)):

            """
            Create Node Potentials if they haven't been traversed to. Excludes the Node Selected by using
            set_index_node_traveled_to_previous
            """
            if index_pseudo_column_node_potential in set_index_node_traveled_to_previous:
                continue

            """
            Skip Finding the Min for the Node Potential if the Node Potential is the Node Child.
            Node Selected == Node Potential == Node Child. The value added to 
            sum_value_min_plus_sum_cost_path_direct_full is added directly and not by finding the min value in the row.

            Basically don't find the cost to yourself. Though if the matrix didn't have 0s on the diagonal, you can
            remove this condition
            """
            if index_pseudo_column_node_potential == index_row_node_selected:
                # Alternative to matrix[index_row_node_selected][index_node_child] is the below:
                # sum_cost_path_direct_full_new = matrix[index_row_node_selected][index_pseudo_column_node_potential]
                # sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full_new
                continue

            # *(Code Difference) Does not need to check if this Node Potential is the Node Starting

            print("\tNode Potential {}".format(index_pseudo_column_node_potential))

            # Current minimum Value (If the code crashes because of this, then my algorithm has a bug)
            value_min = None

            """
            Traverse through current row to select the Min in the row   
            (Code Difference) This loop is now ranged based and now uses pseudo indices
            (THIS WILL CRASH IF MATRIX DOES NOT HAVE THE SAME DIMENSION)
            """
            for index_pseudo_row_node_possible in range(len(matrix[index_pseudo_column_node_potential])):

                # (Code Difference) value_column is explicitly defined
                value_column = matrix[index_pseudo_column_node_potential][index_pseudo_row_node_possible]

                # Skip index_pseudo_row_node_possible if in set_index_node_traveled_to
                if index_pseudo_row_node_possible in set_index_node_traveled_to:
                    continue

                """
                (Code Difference) Replace the old check for this check to see if the Node Potential is the Node 
                Starting (Special case).
                
                This is because Node Starting as a Node Potential DOES NOT know that it has been connected to by
                Node Selected, so you have to Exclude Node Selected as a Node Possible unless a specific condition is
                not met.
                """
                if index_pseudo_column_node_potential == solution_container_current.get_index_node_start():
                    """
                    Check if the size of list_node_path is less than (size of the matrix) -1. The
                    purpose of this check is to only allow its body to run when their are still Node Potentials 
                    excluding the Node Potential that equals the Node Starting.  
                    """
                    if len(solution_container_current.get_entry_list_node_path()) < (len(matrix) - 1):
                        """
                        Basically, when the Node Potential equals the Node Starting while there exists Node Potentials, 
                        excluding the Node Potential that equals the Node Starting, then skip the Node Possible that
                        equals Node Selected.

                        This Condition will not be reached if the Last Node Potential is the Node Potential that equals 
                        the Node Starting.
                        """
                        if index_pseudo_row_node_possible == index_row_node_selected:
                            continue

                # Skip column if the column is on the Diagonal, Comment this out if Diagonals matter.
                if index_pseudo_row_node_possible == index_pseudo_column_node_potential:
                    continue

                # Initialized value_min if there wasn't one to begin with
                if value_min is None:
                    value_min = value_column

                # Select new value_min in current row
                elif value_column < value_min:
                    value_min = value_column

                print("\t\t-> Node Possible {} with Value {}".format(index_pseudo_row_node_possible,
                                                                     value_column))

            sum_value_min_plus_sum_cost_path_direct_full += value_min
            print("\tMinimum Value in column:", value_min)

        print("Sum of Minimum values + Cost of path direct full: {}\n".format(
            sum_value_min_plus_sum_cost_path_direct_full))

        solution_container_new = SolutionContainer(solution_container_current)
        solution_container_new.set_entry_sum_cost_path_complete(sum_value_min_plus_sum_cost_path_direct_full)
        solution_container_new.set_entry_index_node_child(index_row_node_selected)
        solution_container_new.set_entry_sum_cost_path_direct_full(sum_cost_path_direct_full_new)
        solution_container_new.add_to_entry_list_node_path(index_row_node_selected)

        # Add Solution Container to the Priority Queue.
        heapq.heappush(heap_queue_priority, solution_container_new)

        # set_index_node_traveled_to.pop()  # Implicit removal of index_row_node_selected
        # (Code Difference) index_row_node_selected is replaced by index_node_child
        set_index_node_traveled_to.remove(
            solution_container_current.get_entry_index_node_child())  # Explicit removal of index_node_child

    """
    Returning -1 implies that an Upper has been created. Uppers are only made when a path has traversed all nodes 
    and has returned to the Node Starting.
    """
    return -1


@decorator_callable_count(dict_k_callable_v_amount_call_given=dict_k_callable_v_amount_call)
def branch_and_bound_node_exit_entry(matrix,
                                     heap_queue_priority: List[Tuple[int, int, List[int], int]],
                                     solution_container_current: SolutionContainer
                                     ) -> int:
    """
    Notes:
        * index_node is just another way of saying node..

        Node Start:     The Node Starting (index_node_start) of the entire traversal, it is basically the Root Node
                        (e.g. A -> B). There is only 1 Node Starting and that Node is also a Node Target.

        Node Target:    The Node Starting (index_node_parent) that will travel to a Node Selected (e.g. B -> C ).
                        There is only 1 Node Target that is also a Node Starting, but there can be many Node Targets.

        Node Selected:  The Node that the Node Target connects to (e.g. C from the example of B -> C).

        Node Potential: A Node that follow this format: NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        Node Possible:  A Node that is inside the set for a Node Potential.

    :param matrix: Matrix
    :param heap_queue_priority: The Priority Queue
    :param solution_container_current:

    :return:
    """
    """
    set_exit_index_node_traveled_to has the set of nodes used in the traversal except for the Node Starting unless the
    last node to add is the Node Starting.

    We require a copy of set_exit_index_node_traveled_to as set_exit_index_node_traveled_to_previous because 
    set_exit_index_node_traveled_to will be modified to include a Node Selected. 

    set_exit_index_node_traveled_to will be used to prevent a Node in set_exit_index_node_traveled_to from becoming a
    Node Possible. Basically, prevent a Node Possible from being inside of set in a
    NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

    set_exit_index_node_traveled_to_previous will be used to prevent a Node from set_exit_index_node_traveled_to_previous from
    becoming a Node Potential. Example:
        set_exit_index_node_traveled_to = {C, D}     # C and D will not be a NODE_POSSIBLE in the set in the format:
                                                # NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        set_exit_index_node_traveled_to_previous = {D}  # D Will not be a NODE_POTENTIAL
        A -> D -> C = 10
        C -> {B} = 3
        B -> {A} = 2

    """
    set_exit_index_node_traveled_to = set(solution_container_current.get_exit_list_node_path()[
                                          1:])  # TODO UNNCESSSARY BECASE WE FUCK THE SET UP BECAUEAS WE TRAVEL TO ALL OF THEM

    set_entry_index_node_traveled_to = set(solution_container_current.get_entry_list_node_path()[1:])

    set_exit_index_node_traveled_to_previous = set_exit_index_node_traveled_to.copy()

    set_entry_index_node_traveled_to_previous = set_entry_index_node_traveled_to.copy()

    # Parent
    _exit_index_node_parent = solution_container_current.get_exit_index_node_parent()

    # Child
    _entry_index_node_child = solution_container_current.get_entry_index_node_child()

    # Start
    _index_node_start = solution_container_current.get_index_node_start()

    for index_row_node_selected, row_main in enumerate(matrix):

        # # Skip the Node Selected if the Node Selected is the Node Target (Prevent calculations to self).
        # if index_row_node_selected == solution_container_current.get_exit_index_node_parent():
        #     print("SEL PAR")
        #     continue
        #
        # # Skip the Node Selected if the Node Selected has already been traveled to.
        # if index_row_node_selected in set_exit_index_node_traveled_to:
        #     continue

        """
        Skip the Node Selected if the Node Selected is the Node Start (Can't jump to yourself until the end).
        Note that the Node Start is NOT added to index_row_node_selected to make the algorithm easier to use.
        """
        if (index_row_node_selected == solution_container_current.get_index_node_start() and
                (len(solution_container_current.get_exit_list_node_path()) < len(matrix) and
                 len(solution_container_current.get_entry_list_node_path()) < len(matrix)
                )):
            # print("Not the ending")
            continue

        # Initialized sum
        exit_sum_value_min_plus_sum_cost_path_direct_full = 0
        entry_sum_value_min_plus_sum_cost_path_direct_full = 0

        # TODO: DOES NOT BELONG
        """
        Get the Cost of a Full Direct Path
        Example:
            Cost of the Previous Sum Path Direct
              4
            A -> D

            Cost of the New Sum Path Direct
              6
            D -> C

            Cost of the Full Sum Path Direct
              4    6
            A -> D -> C

        """

        # (Code Difference) The Positions of index_row_node_selected and index_node_child are swapped
        exit_sum_cost_path_direct_parent_selected = matrix[_exit_index_node_parent][index_row_node_selected]

        entry_sum_cost_path_direct_selected_child = matrix[index_row_node_selected][_entry_index_node_child]

        exit_sum_cost_path_direct_full_new = (exit_sum_cost_path_direct_parent_selected +
                                              solution_container_current.get_exit_sum_cost_path_direct_full())

        entry_sum_cost_path_direct_full_new = (entry_sum_cost_path_direct_selected_child +
                                               solution_container_current.get_entry_sum_cost_path_direct_full())

        # A Sum of the Sum of the Minimum Value Sum of rows + Sum of the Full Direct Path
        exit_sum_value_min_plus_sum_cost_path_direct_full += exit_sum_cost_path_direct_full_new

        entry_sum_value_min_plus_sum_cost_path_direct_full += entry_sum_cost_path_direct_full_new

        print("(Exit) Node Parent {} -> Node Selected {}: {}".format(_exit_index_node_parent,
                                                                     index_row_node_selected,
                                                                     exit_sum_value_min_plus_sum_cost_path_direct_full))

        # exit_sum_cost_path_direct_full_new = exit_sum_cost_path_direct_parent_selected + solution_container_current.get_entry_index_node_child()

        print("(Entry) Node Selected {} -> Node Child {}: {}".format(index_row_node_selected,
                                                                     _entry_index_node_child,
                                                                     entry_sum_value_min_plus_sum_cost_path_direct_full))

        """
        Add Node Child to set of Nodes traveled to (AKA Set of Nodes Excluded)
        (Code Difference) index_node_child replaces index_row_node_selected
        """

        set_exit_index_node_traveled_to.add(
            index_row_node_selected)  # TODO UNNCESSSARY BECASE WE FUCK THE SET UP BECAUEAS WE TRAVEL TO ALL OF THEM

        set_entry_index_node_traveled_to.add(_index_node_start)
        set_entry_index_node_traveled_to.add(_entry_index_node_child)

        print("set_exit_index_node_traveled_to",
              set_exit_index_node_traveled_to)  # TODO ITS SUPPOSED TO BE BROKEN BECAUSE WE HAVE TO TRAVEL TO ALL OF THE NODES WHCIH FUCKS THE SET
        print("set_exit_index_node_traveled_to_previous", set_exit_index_node_traveled_to_previous)

        print("set_entry_index_node_traveled_to", set_entry_index_node_traveled_to)
        print("set_entry_index_node_traveled_to_previous", set_entry_index_node_traveled_to_previous)

        """
        It's not possible to make Node Potential when every node has been traversed through except for the last node.
        If you assume that the dimensions of the matrix are the same, then you can say that the the size of the matrix
        represents the nodes traversed.

        Basically, you have traversed to every node, so you don't need to loop through the matrix and all you
        really need to do is add list_node_path to the path and you have traveled to every node and have gone
        back to the Node Starting.
        """
        if (len(solution_container_current.get_exit_list_node_path()) == len(matrix) or
                len(solution_container_current.get_entry_list_node_path()) == len(matrix)):
            print("It's Not possible to make Node Potentials")

            solution_container_new = SolutionContainer(solution_container_current)

            solution_container_new.set_exit_sum_cost_path_complete(exit_sum_value_min_plus_sum_cost_path_direct_full)
            solution_container_new.set_exit_index_node_parent(index_row_node_selected)

            if len(solution_container_current.get_exit_list_node_path()) == len(matrix):
                solution_container_new.add_to_exit_list_node_path(index_row_node_selected)

            solution_container_new.set_entry_sum_cost_path_complete(entry_sum_value_min_plus_sum_cost_path_direct_full)
            solution_container_new.set_entry_index_node_child(index_row_node_selected)

            if len(solution_container_current.get_entry_list_node_path()) == len(matrix):
                solution_container_new.add_to_entry_list_node_path(index_row_node_selected)

            # Add Solution Container New to priority queue.
            heapq.heappush(heap_queue_priority, solution_container_new)

            """
            Return the newly created Upper. Uppers are only made when a path has traversed all nodes and has returned 
            to the Node Starting.
            """
            return solution_container_new.get_sum_cost_path_complete()

        # Current minimum Value (If the code crashes because of this, then my algorithm has a bug)
        list_value_min_per_row = [None] * len(matrix)
        list_value_min_per_column = [None] * len(matrix)
        # list_value_min_per_column_when_exit_condition_valid = [None] * len(matrix)

        """
        Loop through rows in the matrix
        (Code Difference) This loop is now ranged based and now uses pseudo indices
        (THIS WILL CRASH IF MATRIX DOES NOT HAVE THE SAME DIMENSION)
        """
        for index_row_node_potential in range(len(matrix)):

            print("\tNode Potential {}".format(index_row_node_potential))

            """
            Traverse through current row to select the Min in the row   
            (Code Difference) This loop is now ranged based and now uses pseudo indices
            (THIS WILL CRASH IF MATRIX DOES NOT HAVE THE SAME DIMENSION)
            """
            for index_column_node_possible in range(len(matrix[index_row_node_potential])):

                exit_condition_valid = True

                entry_condition_valid = True

                value_at_row_column = matrix[index_row_node_potential][index_column_node_possible]

                # Skip column if the column is on the Diagonal, Comment this out if Diagonals matter.
                # POSSIBLE TO POTENTIAL SELF JUMP
                if index_column_node_possible == index_row_node_potential:
                    exit_condition_valid = False
                    entry_condition_valid = False
                    continue

                ########################### ROW ###########################
                ########################### ROW ###########################
                ########################### ROW ###########################
                ########################### ROW ###########################

                # TODO THIS IS FIXED
                # if _index_node_start != _exit_index_node_parent:
                #     # POSSIBLE IS PARENT BUT NOT FOR START
                #     if _exit_index_node_parent == index_column_node_possible:
                #         exit_condition_valid = False

                # SELECTED IN PREVIOUS (WILL ELIMINATE SLEF CALCULATION) (MAKES AN EMPTY SOLUTION)
                if index_row_node_selected in set_exit_index_node_traveled_to_previous:
                    exit_condition_valid = False
                    continue
                # POTENTIAL IN PREVIOUS
                if index_row_node_potential in set_exit_index_node_traveled_to_previous:
                    exit_condition_valid = False
                    continue
                # POTENTIAL IS PARENT
                if index_row_node_potential == _exit_index_node_parent:
                    exit_condition_valid = False
                    continue

                # POTENTIAL FOR THE END
                if (index_row_node_potential == _index_node_start and
                        len(solution_container_current.get_exit_list_node_path()) < len(matrix)):
                    # print("index_row_node_potential is index_node_start, but is not the Last Node to yourself")
                    exit_condition_valid = False
                    continue

                """
                Special condition for when index_row_node_selected == index_row_node_potential. This condition is to
                prevent index_row_node_potential from connecting back to what is connecting to it.
                """
                if index_row_node_potential == index_row_node_selected:
                    """
                    The body of the following condition should only run when the Node Potentials, other than the Node
                    Selected, have exhausted their Node Possibles. If there are no Node Possibles for the Node
                    Potentials that does not include the Node Selected, then the Node Potential that is also the
                    Node Selected is allowed to make the last connection to the last Node Possible which should be
                    Node Starting.
                    """

                    if len(solution_container_current.get_exit_list_node_path()) < (len(matrix) - 1):
                        """
                        Check if index_node_parent is index_column_node_possible, if this condition is true, then
                        index_row_node_selected should not calculate the distance for index_column_node_possible. If
                        the calculation from index_row_node_potential to index_column_node_possible is allowed, then
                        it's possible for index_column_node_possible to connect back to its parent which should be
                        index_row_node_potential.
                        Example:
                            A -> B = 3
                            B -> {C, D, A} = 1  # You don't want B to connect back to A because A already points to B
                            C -> {A, D} = 5
                            D -> {A, C} = 6
                        """
                        if index_column_node_possible == solution_container_current.get_index_node_start():
                            exit_condition_valid = False
                            continue

                # POSSIBLE IN THE SET (WE DONT HAVE SET ANYMORE) ***************************
                if (index_column_node_possible in set_exit_index_node_traveled_to_previous or
                        index_column_node_possible == index_row_node_selected):
                    exit_condition_valid = False
                    continue

                if exit_condition_valid:
                    pass
                    print("\t\t-> (Exit) Node Possible {} with Value {}".format(
                        index_column_node_possible,
                        value_at_row_column))

                    # ROW ASSIGNER
                    if list_value_min_per_row[index_row_node_potential] is None:
                        list_value_min_per_row[index_row_node_potential] = value_at_row_column

                    elif value_at_row_column < list_value_min_per_row[index_row_node_potential]:
                        list_value_min_per_row[index_row_node_potential] = value_at_row_column

                ########################### COLUMN ###########################
                ########################### COLUMN ###########################
                ########################### COLUMN ###########################
                ########################### COLUMN ###########################

                # print(f"\n{'#'*100}\n")
                # print("VALUE PER ROW")

                # SELECTED IN SET
                if index_row_node_selected in set_entry_index_node_traveled_to:
                    entry_condition_valid = False

                # POTENTIAL IN SET PREVIOUS # TODO???
                if index_row_node_potential in set_entry_index_node_traveled_to_previous:
                    entry_condition_valid = False

                # POTENTIAL IS SELECTED
                if index_row_node_potential == index_row_node_selected:
                    entry_condition_valid = False

                """
                (Code Difference) Replace the old check for this check to see if the Node Potential is the Node
                Starting (Special case).

                This is because Node Starting as a Node Potential DOES NOT know that it has been connected to by
                Node Selected, so you have to Exclude Node Selected as a Node Possible unless a specific condition is
                not met.
                """
                if index_row_node_potential == _index_node_start:
                    """
                    Check if the size of list_node_path is less than (size of the matrix) -1. The
                    purpose of this check is to only allow its body to run when their are still Node Potentials
                    excluding the Node Potential that equals the Node Starting.
                    """
                    if len(solution_container_current.get_entry_list_node_path()) < (len(matrix) - 1):
                        """
                        Basically, when the Node Potential equals the Node Starting while there exists Node Potentials,
                        excluding the Node Potential that equals the Node Starting, then skip the Node Possible that
                        equals Node Selected.

                        This Condition will not be reached if the Last Node Potential is the Node Potential that equals
                        the Node Starting.
                        """
                        if index_column_node_possible == index_row_node_selected:
                            entry_condition_valid = False

                # POTENTIAL AS SELECTED
                if index_row_node_potential == index_row_node_selected:
                    entry_condition_valid = False

                # POSSIBLE IN THE SET
                if index_column_node_possible in set_entry_index_node_traveled_to:
                    entry_condition_valid = False

                # POTENTIAL IS POSSIBLE
                if index_row_node_potential == index_column_node_possible:
                    entry_condition_valid = False

                if entry_condition_valid:
                    pass
                    print("\t\t-> (Entry) Node Possible {} with Value {}".format(
                        index_column_node_possible,
                        value_at_row_column))

                    # COLUMN ASSIGNER
                    if list_value_min_per_column[index_row_node_potential] is None:
                        list_value_min_per_column[index_row_node_potential] = value_at_row_column

                    elif value_at_row_column < list_value_min_per_column[index_row_node_potential]:
                        list_value_min_per_column[index_row_node_potential] = value_at_row_column

                    if exit_condition_valid:
                        pass

                #################################
                #################################

        sum_list_value_min_per_row = 0
        sum_list_value_min_per_column = 0

        for i, j in zip(list_value_min_per_row, list_value_min_per_column):
            if isinstance(i, int):
                sum_list_value_min_per_row += i
            if isinstance(j, int):
                sum_list_value_min_per_column += j

        exit_sum_value_min_plus_sum_cost_path_direct_full += sum_list_value_min_per_row
        entry_sum_value_min_plus_sum_cost_path_direct_full += sum_list_value_min_per_column

        print("\tMinimum Value in row:", list_value_min_per_row)
        print("\tSum Minimum Value in row:", sum_list_value_min_per_row)
        print("\tMinimum Value in column:", list_value_min_per_column)
        print("\tSum Minimum Value in column:", sum_list_value_min_per_column)
        print("\tMinimum Value in row + Minimum Value in column:",
              sum_list_value_min_per_row + sum_list_value_min_per_column)
        print("(Exit) Sum of Minimum values + Cost of path direct full: {}".format(
            exit_sum_value_min_plus_sum_cost_path_direct_full))
        print("(Entry) Sum of Minimum values + Cost of path direct full: {}".format(
            entry_sum_value_min_plus_sum_cost_path_direct_full))
        print("(Exit + Entry) Sum of Minimum values + Cost of path direct full: {}".format(
            exit_sum_value_min_plus_sum_cost_path_direct_full + entry_sum_value_min_plus_sum_cost_path_direct_full)
        )
        exit_sum_value_min_plus_sum_cost_path_direct_full_plus_sum_list_value_min_per_column = (
                exit_sum_value_min_plus_sum_cost_path_direct_full + sum_list_value_min_per_column
        )
        print("(Exit) Sum of Minimum values + Cost of path direct full + Sum Minimum Value in column: {}".format(
            exit_sum_value_min_plus_sum_cost_path_direct_full_plus_sum_list_value_min_per_column))
        print()

        solution_container_new = SolutionContainer(solution_container_current)

        # solution_container_new.set_exit_sum_cost_path_complete(exit_sum_value_min_plus_sum_cost_path_direct_full)
        solution_container_new.set_exit_sum_cost_path_complete(
            exit_sum_value_min_plus_sum_cost_path_direct_full_plus_sum_list_value_min_per_column)
        solution_container_new.set_exit_index_node_parent(index_row_node_selected)
        solution_container_new.set_exit_sum_cost_path_direct_full(exit_sum_cost_path_direct_full_new)
        solution_container_new.add_to_exit_list_node_path(index_row_node_selected)

        # solution_container_new.set_entry_sum_cost_path_complete(entry_sum_value_min_plus_sum_cost_path_direct_full)
        # solution_container_new.set_entry_index_node_child(index_row_node_selected)
        # solution_container_new.set_entry_sum_cost_path_direct_full(entry_sum_cost_path_direct_full_new)
        # solution_container_new.add_to_entry_list_node_path(index_row_node_selected)

        # # TODO NEED TO REMOVE ME LATER TO WORK PROPERLY
        if (exit_sum_value_min_plus_sum_cost_path_direct_full > exit_sum_cost_path_direct_full_new):
            # Add Solution Container to the Priority Queue.
            heapq.heappush(heap_queue_priority, solution_container_new)
            # print(heap_queue_priority)

        # if (entry_sum_value_min_plus_sum_cost_path_direct_full != entry_sum_cost_path_direct_full_new):
        #     # Add Solution Container to the Priority Queue.
        #     heapq.heappush(heap_queue_priority, solution_container_new)
        #     # print(heap_queue_priority)

        # set_exit_index_node_traveled_to.pop()  # Implicit removal of index_row_node_selected
        set_exit_index_node_traveled_to.remove(index_row_node_selected)  # Explicit removal of index_node_child
        set_entry_index_node_traveled_to.remove(_entry_index_node_child)  # Explicit removal of index_node_child

    """
    Returning -1 implies that an Upper has been created. Uppers are only made when a path has traversed all nodes 
    and has returned to the Node Starting.
    """
    return -1


@decorator_callable_count(dict_k_callable_v_amount_call_given=dict_k_callable_v_amount_call)
def branch_and_bound_bfs_priority_queue(matrix: Sequence[Sequence[int]],
                                        index_node_start: int = 0,
                                        function_branch_and_bound=branch_and_bound_node_exit
                                        ):
    heap_queue_priority: Union[List[SolutionContainer], List] = []
    upper = -1

    list_solutions: Union[List[SolutionContainer], List] = []

    is_initial_run = True

    while heap_queue_priority or is_initial_run:

        path_solution_temp: Union[SolutionContainer, None] = None

        # tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct: Union[Tuple[int, int, List, int],
        #                                                                              None] = None

        # Select a Solution Container from the Priority Queue if an Upper is found
        if upper != -1:
            print("Upper Exists, Will Trim and Select from the Priority Queue")

            # Select from the priority queue a Solution Container's Sum Total == Upper
            path_solution_temp = heapq.heappop(heap_queue_priority)

            print("Solution Container Currently Selected",
                  path_solution_temp)

            # Less than or equal to will allow errors to pass for me to make sure i'm doing the right operations
            if path_solution_temp.get_sum_cost_path_complete() <= upper:
                print(path_solution_temp)
                print("Solution Container Currently Selected Is valid")
            else:
                print("Solution Container Currently Selected Is invalid")
                continue

        # Select a Solution Container from the Priority Queue if not empty (If this crashes then there is a bug)
        elif heap_queue_priority:
            path_solution_temp = heapq.heappop(heap_queue_priority)
            print("No Upper Exists, Will Pop from Solution Container from the Priority Queue:",
                  path_solution_temp)

        # If a Solution Container is Selected
        if path_solution_temp:

            # Initialize temp variables for ease of use
            # sum_total_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[0]
            # index_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[1]
            # list_node_path_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[2]
            # sum_direct_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[3]

            # If list_node_path has traversed every node and has reached the end.
            if (len(path_solution_temp.get_entry_list_node_path()) == (len(matrix) + 1) or
                    len(path_solution_temp.get_exit_list_node_path()) == (len(matrix) + 1)):

                print("Solution Container may be a Valid Solution")

                # If a Actual Solution
                if path_solution_temp.get_sum_cost_path_complete() == upper:
                    print("Solution Container is a Valid Solution")
                    print(heap_queue_priority)
                    print(path_solution_temp)
                    print()

                    list_solutions.append(path_solution_temp)
                continue

            # New Style (If this crashes then there is a bug)
            # set_index_node_traveled_to = set(list_node_path_selected[1:])

            # # Fill up set based on list_node_path_selected
            # for i in range(1, len(list_node_path_selected)):
            #     set_index_node_traveled_to.add(list_node_path_selected[i])

        # If a Solution Container is not Selected. This is the initial run, it is only ran once.
        else:
            # Allow the Main while loop to exit if the Priority Queue is empty
            is_initial_run = False

            # Initialize Defaults
            # sum_total_selected = 0
            # index_selected = index_node_start
            # list_node_path_selected = [index_parent]
            # sum_direct_selected = 0
            # # set_index_node_traveled_to = set()

            path_solution_temp = SolutionContainer(index_node_start)

        ##################################################################################################

        # print("\nPath Selected:", list_node_path_selected)
        print("STUFF OVER HERE", path_solution_temp)

        upper_potential = function_branch_and_bound(matrix,
                                                    heap_queue_priority,
                                                    path_solution_temp
                                                    )

        # If an Upper has been returned
        if upper_potential != -1:
            # Initialize first Upper
            if upper == -1:
                upper = upper_potential

            # Every New Upper
            elif upper_potential < upper:
                upper = upper_potential

        print(heap_queue_priority)
        print("-" * 100)
        print()

        ##################################################################################################

    return list_solutions


def main():
    example_1()
    print(f"\n{'#' * 150}\n")
    # example_2()


def example_tester(matrix):
    # print("Consider Exit Only Solution")
    # solutions_exit = branch_and_bound_bfs_priority_queue(matrix,
    #                                                      function_branch_and_bound=branch_and_bound_node_exit)
    # print(f"\n{'=' * 200}\n")
    #
    # print("Consider Entry Only Solution")
    # solutions_entry = branch_and_bound_bfs_priority_queue(matrix,
    #                                                       function_branch_and_bound=branch_and_bound_node_entry)
    # print(f"\n{'=' * 200}\n")

    print("Consider Exit and Entry (Exit is Priority) Solution")
    solutions_exit_entry = branch_and_bound_bfs_priority_queue(matrix,
                                                               function_branch_and_bound=branch_and_bound_node_exit_entry)
    print(f"\n{'=' * 200}\n")

    print("Matrix:")
    print(numpy.array(matrix), end="\n")
    print()

    # print("Solution Containers (Exit only)")
    # for i in solutions_exit:
    #     print(i)
    # print()
    #
    # print("Solution Containers (Entry only)")
    # for i in solutions_entry:
    #     print(i)
    # print()

    print("Solution Containers (Exit and Entry (Exit is Priority))")
    for i in solutions_exit_entry:
        print(i)
    print()

    print("Callable Call Count")
    print("{:<5}{:<40}{}".format("", "Callable", "Call Count"))
    for k, v in dict_k_callable_v_amount_call.items():
        print("{:<5}{:<40}{}".format("", k, v))

    # print(pandas.DataFrame.from_dict(dict_k_callable_v_amount_call,
    #                                  orient='index',
    #                                  columns=["Call count"]))

    # df = pandas.DataFrame(dict_k_callable_v_amount_call.items(), columns=["Callable", "Call count"])
    # df.style.set_properties(**{'text-align': 'right'})
    # print(df)


def example_1():
    matrix = [[0, 3, 7, 4],
              [2, 0, 5, 1],
              [9, 3, 0, 5],
              [8, 7, 6, 0]]
    example_tester(matrix)


def example_2():
    matrix = [[0, 14, 4, 10, 20],
              [14, 0, 7, 8, 7],
              [4, 5, 0, 7, 16],
              [11, 7, 9, 0, 2],
              [18, 7, 17, 4, 0]]
    example_tester(matrix)


if __name__ == '__main__':
    main()
