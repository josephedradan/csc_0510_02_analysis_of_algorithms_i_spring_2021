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

"""
import heapq
import numpy
from typing import Sequence, List, Tuple, Union, Set


# def solve_exit_node_first_dynamic_programming(matrix: Sequence[Sequence]):
#     pass


def branch_and_bound_node_exit(matrix,
                               heap_queue_priority: List[Tuple[int, int, List[int], int]],
                               index_node_start: int,
                               index_node_parent: int,
                               set_index_node_traveled_to: Set[int],
                               list_node_path: List[int],
                               sum_node_path_direct_previous: int,
                               ) -> int:
    """
    Notes:
        * index_node is just another way of saying node..

        Node Start:     The Starting Node (index_node_start) of the entire traversal, it is basically the Root Node
                        (e.g. A -> B). There is only 1 Starting Node and that Node is also a Node Parent.

        Node Parent:    The Starting Node (index_node_parent) that will travel to a Node Selected (e.g. B -> C ).
                        There is only 1 Node Parent that is also a Starting Node, but there can be many Node Parents.

        Node Selected:  The Node that the Node Parent connects to (e.g. C from the example of B -> C).

        Node Potential: A Node that follow this format: NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        Node Possible:  A Node that is inside the set for a Node Potential.

    :param matrix: Matrix
    :param heap_queue_priority: The Priority Queue
    :param index_node_start: Staring Node or index of the Starting Node (Same thing)
    :param index_node_parent: Parent Node or index of the Parent Node (Same thing)
    :param set_index_node_traveled_to: Set of indices traversed (Set of nodes traversed0
    :param list_node_path: List that represents the Order of Nodes to traverse that has the minimum cost
    :param sum_node_path_direct_previous: Previous Sum of the Direct Path
    :return:
    """
    """
    set_index_node_traveled_to has the set of nodes used in the traversal except for the starting node unless the
    last node to add is the starting node.
    
    We require a copy of set_index_node_traveled_to as set_index_node_traveled_to_previous because 
    set_index_node_traveled_to will be modified to include a Node Selected. 
    
    set_index_node_traveled_to will be used to prevent a Node in set_index_node_traveled_to from becoming a
    Node Possible. Basically, prevent a Node Possible from being inside of set in a
    NODE_POTENTIAL -> {NODE_POSSIBLE, ...}
    
    set_index_node_traveled_to_previous will be used to prevent a Node from set_index_node_traveled_to_previous from
    becoming a Node Potential. Example:
        set_index_node_traveled_to = {C, D}     # C and D will not be a NODE_POSSIBLE in the set in the format:
                                                # NODE_POTENTIAL -> {NODE_POSSIBLE, ...}
                                                
        set_index_node_traveled_to_previous = {D}  # D Will not be a NODE_POTENTIAL
        A -> D -> C = 10
        C -> {B} = 3
        B -> {A} = 2
    
    """
    set_index_node_traveled_to_previous = set_index_node_traveled_to.copy()

    for index_row_node_selected, row_main in enumerate(matrix):

        # Skip the Node Selected if the Node Selected is the Node Parent (Prevent calculations to self).
        if index_row_node_selected == index_node_parent:
            continue

        # Skip the Node Selected if the Node Selected has already been traveled to.
        if index_row_node_selected in set_index_node_traveled_to:
            continue

        """
        Skip the Node Selected if the Node Selected is the Node Start (Can't jump to yourself until the end).
        Note that the Node Start is NOT added to index_row_node_selected to make the algorithm easier to use.
        """
        if index_row_node_selected == index_node_start and len(list_node_path) < len(matrix):
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
        sum_cost_path_direct_new = matrix[index_node_parent][index_row_node_selected]

        sum_cost_path_direct_full = sum_cost_path_direct_new + sum_node_path_direct_previous

        # A Sum of the Sum of the Minimum Value Sum of rows + Sum of the Full Direct Path
        sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full

        print("Node Parent {} -> Node Selected {}: {}".format(index_node_parent, index_row_node_selected,
                                                              sum_value_min_plus_sum_cost_path_direct_full))

        # Add Node Selected to set of Nodes traveled to (AKA Set of Nodes Excluded)
        set_index_node_traveled_to.add(index_row_node_selected)

        print("set_index_node_traveled_to", set_index_node_traveled_to)
        print("set_index_node_traveled_to_previous", set_index_node_traveled_to_previous)

        """
        It's not possible to make Node Potential when every node has been traversed through except for the last node.
        If you assume that the dimensions of the matrix are the same, then you can say that the the size of the matrix
        represents the nodes traversed.
        
        Basically, you have you have traversed to every node, so you don't need to loop through the matrix and all you
        really need to do is add index_row_node_selected to the path and you have traveled to every node and have gone
        back to the Starting Node.
        """
        if len(set_index_node_traveled_to) == len(matrix):

            print("It's Not possible to make Node Potentials")

            # Create a new Tuple Solution
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct = (sum_value_min_plus_sum_cost_path_direct_full,
                                                                  index_row_node_selected,
                                                                  [],
                                                                  0)

            """
            Add the Nodes from the current list_node_path to a new list_node_path
            It's a tuple, you can't copy the list_node_path, you need to loop and append to the list
            """
            for i in list_node_path:
                tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(i)

            # Add the current index_row_node_selected to the list_node_path, can't use the set because it's not in order
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_row_node_selected)

            # Add tuple to priority queue.
            heapq.heappush(heap_queue_priority, tuple_0_sum_total_1_index_2_list_path_3_sum_direct)

            """
            Return the newly created Upper. Uppers are only made when a path has traversed all nodes and has returned 
            to the Starting Node.
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
            if index_row_node_potential == index_node_parent:
                # Alternative to matrix[index_node_parent][index_row_node_selected] is the below:
                # sum_cost_path_direct_full = matrix[index_row_node_potential][index_row_node_selected]
                # sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full
                continue

            """
            Basically, If index_row_node_potential is the Starting Node, but the index_row_node_potential is not the
            last node to traverse to (last node to traverse to is yourself), then index_row_node_potential is not a 
            Node Potential.
            """
            if index_row_node_potential == index_node_start and len(list_node_path) < len(matrix):
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
        print("Sum of Minimum values + Cost of Node Selected: {}\n".format(
            sum_value_min_plus_sum_cost_path_direct_full))

        # Create a new Tuple Solution
        tuple_0_sum_total_1_index_2_list_path_3_sum_direct = (sum_value_min_plus_sum_cost_path_direct_full,
                                                              index_row_node_selected,
                                                              [],
                                                              sum_cost_path_direct_full)

        # If no initial list_node_path is given to this algorithm.
        if list_node_path is None:
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_node_start)

        # If an initial list_node_path is given.
        else:
            # It's a tuple, you can't copy the list_node_path, you need to loop and add.
            for i in list_node_path:
                tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(i)

        # Append index_row_node_selected to the new list_node_path in the Tuple Solution
        tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_row_node_selected)

        # Add Tuple Solution to the Priority Queue.
        heapq.heappush(heap_queue_priority, tuple_0_sum_total_1_index_2_list_path_3_sum_direct)
        # print(heap_queue_priority)

        # set_index_node_traveled_to.pop()  # Implicit removal of index_row_node_selected
        set_index_node_traveled_to.remove(index_row_node_selected)  # Explicit removal of index_row_node_selected

    """
    Returning -1 implies that an Upper has been created. Uppers are only made when a path has traversed all nodes 
    and has returned to the Starting Node.
    """
    return -1


def branch_and_bound_node_entry(matrix,
                                heap_queue_priority: List[Tuple[int, int, List[int], int]],
                                index_node_start: int,
                                index_node_parent: int,
                                set_index_node_traveled_to: Set[int],
                                list_node_path: List[int],
                                sum_node_path_direct_previous: int,
                                ) -> int:
    """
    Notes:
        * index_node is just another way of saying node..

        Node Start:     The Starting Node (index_node_start) of the entire traversal, it is basically the Root Node
                        (e.g. A -> B). There is only 1 Starting Node and that Node is also a Node Parent.

        Node Parent:    The Starting Node (index_node_parent) that will travel to a Node Selected (e.g. B -> C ).
                        There is only 1 Node Parent that is also a Starting Node, but there can be many Node Parents.

        Node Selected:  The Node that the Node Parent connects to (e.g. C from the example of B -> C).

        Node Potential: A Node that follow this format: NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        Node Possible:  A Node that is inside the set for a Node Potential.

    :param matrix: Matrix
    :param heap_queue_priority: The Priority Queue
    :param index_node_start: Staring Node or index of the Starting Node (Same thing)
    :param index_node_parent: Parent Node or index of teh Parent Node (Same thing)
    :param set_index_node_traveled_to: Set of indices traversed (Set of nodes traversed0
    :param list_node_path: List that represents the Order of Nodes to traverse that has the minimum cost
    :param sum_node_path_direct_previous: Previous Sum of the Direct Path
    :return:
    """
    """
    set_index_node_traveled_to has the set of nodes used in the traversal except for the starting node unless the
    last node to add is the starting node.

    We require a copy of set_index_node_traveled_to as set_index_node_traveled_to_previous because 
    set_index_node_traveled_to will be modified to include a Node Selected. 

    set_index_node_traveled_to will be used to prevent a Node in set_index_node_traveled_to from becoming a
    Node Possible. Basically, prevent a Node Possible from being inside of set in a
    NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

    set_index_node_traveled_to_previous will be used to prevent a Node from set_index_node_traveled_to_previous from
    becoming a Node Potential. Example:
        set_index_node_traveled_to = {C, D}     # C and D will not be a NODE_POSSIBLE in the set in the format:
                                                # NODE_POTENTIAL -> {NODE_POSSIBLE, ...}

        set_index_node_traveled_to_previous = {D}  # D Will not be a NODE_POTENTIAL
        A -> D -> C = 10
        C -> {B} = 3
        B -> {A} = 2

    """
    set_index_node_traveled_to_previous = set_index_node_traveled_to.copy()

    for index_row_node_selected, row_main in enumerate(matrix):

        # Skip the Node Selected if the Node Selected is the Node Parent (Prevent calculations to self).
        if index_row_node_selected == index_node_parent:
            continue

        # Skip the Node Selected if the Node Selected has already been traveled to.
        if index_row_node_selected in set_index_node_traveled_to:
            continue

        """
        Skip the Node Selected if the Node Selected is the Node Start (Can't jump to yourself until the end).
        Note that the Node Start is NOT added to index_row_node_selected to make the algorithm easier to use.
        """
        if index_row_node_selected == index_node_start and len(list_node_path) < len(matrix):
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
        sum_cost_path_direct_new = matrix[index_row_node_selected][
            index_node_parent]  # TODO: SWAP WITH index_row_node_selected

        sum_cost_path_direct_full = sum_cost_path_direct_new + sum_node_path_direct_previous

        # A Sum of the Sum of the Minimum Value Sum of rows + Sum of the Full Direct Path
        sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full

        print("Node Parent {} -> Node Selected {}: {}".format(index_node_parent, index_row_node_selected,
                                                              sum_value_min_plus_sum_cost_path_direct_full))

        # Add Node Selected to set of Nodes traveled to (AKA Set of Nodes Excluded)
        set_index_node_traveled_to.add(index_node_parent)  # TODO: SWAP WITH index_row_node_selected

        print("set_index_node_traveled_to", set_index_node_traveled_to)
        print("set_index_node_traveled_to_previous", set_index_node_traveled_to_previous)

        """
        It's not possible to make Node Potential when every node has been traversed through except for the last node.
        If you assume that the dimensions of the matrix are the same, then you can say that the the size of the matrix
        represents the nodes traversed.

        Basically, you have you have traversed to every node, so you don't need to loop through the matrix and all you
        really need to do is add index_row_node_selected to the path and you have traveled to every node and have gone
        back to the Starting Node.
        """
        if len(set_index_node_traveled_to) == len(matrix):

            print("It's Not possible to make Node Potentials")

            # Create a new Tuple Solution
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct = (sum_value_min_plus_sum_cost_path_direct_full,
                                                                  index_row_node_selected,
                                                                  [],
                                                                  0)

            """
            Add the Nodes from the current list_node_path to a new list_node_path
            It's a tuple, you can't copy the list_node_path, you need to loop and append to the list
            """
            for i in list_node_path:
                tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(i)

            # Add the current index_row_node_selected to the list_node_path, can't use the set because it's not in order
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_row_node_selected)

            # Add tuple to priority queue.
            heapq.heappush(heap_queue_priority, tuple_0_sum_total_1_index_2_list_path_3_sum_direct)

            """
            Return the newly created Upper. Uppers are only made when a path has traversed all nodes and has returned 
            to the Starting Node.
            """
            return sum_value_min_plus_sum_cost_path_direct_full

        # matrix = numpy.array(matrix).transpose()

        # Loop through rows in the matrix
        for index_row_node_potential_COLUMN in range(len(matrix)):

            """
            Create Node Potentials if they haven't been traversed to. Excludes the Node Selected by using
            set_index_node_traveled_to_previous
            """
            if index_row_node_potential_COLUMN in set_index_node_traveled_to_previous:
                continue

            """
            Skip Finding the Min for the Node Potential if the Node Potential is the Node Parent.
            Node Selected == Node Potential == Node Parent. The value added to 
            sum_value_min_plus_sum_cost_path_direct_full is added directly and not by finding the min value in the row.

            Basically don't find the cost to yourself. Though if the matrix didn't have 0s on the diagonal, you can
            remove this condition
            """
            if index_row_node_potential_COLUMN == index_node_parent:
                # Alternative to matrix[index_node_parent][index_row_node_selected] is the below:
                # sum_cost_path_direct_full = matrix[index_row_node_potential_COLUMN][index_row_node_selected]
                # sum_value_min_plus_sum_cost_path_direct_full += sum_cost_path_direct_full
                continue

            """
            Basically, If index_row_node_potential_COLUMN is the Starting Node, but the index_row_node_potential_COLUMN is not the
            last node to traverse to (last node to traverse to is yourself), then index_row_node_potential_COLUMN is not a 
            Node Potential.
            """
            if index_row_node_potential_COLUMN == index_node_start and len(list_node_path) < len(matrix):
                print("index_row_node_potential_COLUMN is index_node_start, but is not the Last Node to yourself")
                continue

            print("\tNode Potential {}".format(index_row_node_potential_COLUMN))

            # Current minimum Value (If the code crashes because of this, then my algorithm has a bug)
            value_min = None

            # Traverse through current row to select the Min in the row
            for index_column_node_possible_ROW, value_column in enumerate(row):

                # Skip index_column_node_possible_ROW if in set_index_node_traveled_to
                if index_column_node_possible_ROW in set_index_node_traveled_to:
                    continue

                # Skip column if the column is on the Diagonal, Comment this out if Diagonals matter.
                if index_column_node_possible_ROW == index_row_node_potential_COLUMN:
                    continue

                # Initialized value_min if there wasn't one to begin with
                if value_min is None:
                    value_min = value_column

                # Select new value_min in current row
                elif value_column < value_min:
                    value_min = value_column

                print("\t\t-> Node Possible {} with Value {}".format(index_column_node_possible_ROW, value_column))

            sum_value_min_plus_sum_cost_path_direct_full += value_min

            print("\tMinimum Value in row:", value_min)
        print("Sum of Minimum values + Cost of Node Selected: {}\n".format(
            sum_value_min_plus_sum_cost_path_direct_full))

        # Create a new Tuple Solution
        tuple_0_sum_total_1_index_2_list_path_3_sum_direct = (sum_value_min_plus_sum_cost_path_direct_full,
                                                              index_row_node_selected,
                                                              [],
                                                              sum_cost_path_direct_full)

        # If no initial list_node_path is given to this algorithm.
        if list_node_path is None:
            tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_node_start)

        # If an initial list_node_path is given.
        else:
            # It's a tuple, you can't copy the list_node_path, you need to loop and add.
            for i in list_node_path:
                tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(i)

        # Append index_row_node_selected to the new list_node_path in the Tuple Solution
        tuple_0_sum_total_1_index_2_list_path_3_sum_direct[2].append(index_row_node_selected)

        # Add Tuple Solution to the Priority Queue.
        heapq.heappush(heap_queue_priority, tuple_0_sum_total_1_index_2_list_path_3_sum_direct)
        # print(heap_queue_priority)

        # set_index_node_traveled_to.pop()  # Implicit removal of index_row_node_selected
        set_index_node_traveled_to.remove(
            index_node_parent)  # Explicit removal of index_row_node_selected # TODO: SWAP WITH index_row_node_selected

    """
    Returning -1 implies that an Upper has been created. Uppers are only made when a path has traversed all nodes 
    and has returned to the Starting Node.
    """
    return -1


def branch_and_bound_bfs_priority_queue(matrix: Sequence[Sequence[int]],
                                        index_node_start: int = 0,
                                        function_branch_and_bound=branch_and_bound_node_exit
                                        ):
    heap_queue_priority = []
    index_parent = index_node_start

    upper = -1

    list_solutions = []

    is_initial_run = True

    while heap_queue_priority or is_initial_run:

        tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct: Union[Tuple[int, int, List, int],
                                                                                     None] = None

        # SELECT A TUPLE ON KILL
        if upper != -1:
            print("Upper Exists, Will Trim and Select from the Priority Queue")

            # KILL SELECTING
            while heap_queue_priority:
                tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct = heapq.heappop(
                    heap_queue_priority)
                print("Tuple Solution Currently Selected",
                      tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct)
                if tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[0] <= upper:
                    print(tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct)
                    print("Tuple Solution Currently Selected Is valid")
                    break

        # Select a Tuple Solution from the Priority Queue if not empty (If this crashes then there is a bug)
        elif heap_queue_priority:
            tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct = heapq.heappop(heap_queue_priority)
            print("No Upper Exists, Will Pop from Tuple Solution from the Priority Queue:",
                  tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct)

        # If a Tuple Solution is Selected
        if tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct:

            # Initialize temp variables for ease of use
            sum_total_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[0]
            index_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[1]
            list_node_path_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[2]
            sum_direct_selected = tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[3]

            # If list_node_path has traversed every node and has reached the end.
            if len(list_node_path_selected) == (len(matrix) + 1):
                print("Tuple Solution maybe a Valid Solution")

                # If a Actual Solution
                if tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct[0] == upper:
                    print("Tuple Solution is a Valid Solution")
                    print(heap_queue_priority)
                    print(tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct)
                    print()

                    list_solutions.append(tuple_selected_0_sum_total_1_index_2_list_node_path_3_sum_path_direct)
                continue

            # Initialize Set of Nodes traversed based on the path
            # set_index_node_traveled_to = set()

            # New Style (If this crashes then there is a bug)
            set_index_node_traveled_to = set(list_node_path_selected[1:])

            # # Fill up set based on list_node_path_selected
            # for i in range(1, len(list_node_path_selected)):
            #     set_index_node_traveled_to.add(list_node_path_selected[i])

        # If a Tuple Solution is not Selected. This is the initial run, it is only ran once.
        else:
            # Allow the Main while loop to exit if the Priority Queue is empty
            is_initial_run = False

            # Initialize Defaults
            sum_total_selected = 0
            index_selected = index_node_start
            list_node_path_selected = [index_parent]
            sum_direct_selected = 0
            set_index_node_traveled_to = set()

        ##################################################################################################

        print("\nPath Selected:", list_node_path_selected)

        upper_potential = function_branch_and_bound(matrix,
                                                    heap_queue_priority,
                                                    index_node_start,
                                                    index_selected,
                                                    set_index_node_traveled_to,
                                                    list_node_path_selected,
                                                    sum_direct_selected,
                                                    )

        # If an Upper has been returned
        if upper_potential != -1:

            # Initialize first Upper
            if upper == -1:
                upper = upper_potential

            # Every New Upper.
            elif upper_potential < upper:
                upper = upper_potential

        print(heap_queue_priority)
        print("-" * 100)
        print()

        ##################################################################################################

    return list_solutions


def main():
    example_1()
    # print(f"\n{'#' * 150}\n")
    # example_2()


def example_2():
    matrix = [[0, 14, 4, 10, 20],
              [14, 0, 7, 8, 7],
              [4, 5, 0, 7, 16],
              [11, 7, 9, 0, 2],
              [18, 7, 17, 4, 0]]

    x = branch_and_bound_bfs_priority_queue(matrix)

    print(f"\n{'=' * 100}\n")
    print("Matrix:")
    print(numpy.array(matrix), end="\n\n")
    print("Tuple Solutions")
    for i in x:
        print(i)


def example_1():
    matrix = [[0, 3, 7, 4],
              [2, 0, 5, 1],
              [9, 3, 0, 5],
              [8, 7, 6, 0]]

    x = branch_and_bound_bfs_priority_queue(matrix, function_branch_and_bound=branch_and_bound_node_exit)

    print(f"\n{'=' * 100}\n")
    print("Matrix:")
    print(numpy.array(matrix), end="\n\n")
    print("Tuple Solutions")
    for i in x:
        print(i)


if __name__ == '__main__':
    main()
