'''
EECS 510 - Final Project
Finite Automaton Implementation
Authors: Ahmad Awan

Description:
This is the updated version of the old EECS 510 project. All contributions are made by Ahmad Awan solely.
The code now implements a Pushdown Automaton (PDA) instead of a Finite Automaton (FA). The PDA is defined by a configuration file.
The PDA also processes parentheses, as compared to the FA which only processed numbers and operators. 
'''

class PushdownAutomaton:  # Define a class to represent a Pushdown Automaton
    def __init__(self, config_file):  # Constructor to initialize the automaton
        self.states = set()  # Set to store states of the automaton
        self.input_symbols = set()  # Set to store input symbols
        self.stack_symbols = set()  # Set to store stack symbols
        self.start_state = None  # Variable to store the start state
        self.accept_states = set()  # Set to store accepting states
        self.transitions = {}  # Dictionary to store transition rules

        # Parse the configuration file to initialize automaton components
        self._load_from_file(config_file)

    def _load_from_file(self, config_file):  # Private method to load configuration from a file
        with open(config_file, 'r') as file:  # Open the configuration file for reading
            lines = file.readlines()  # Read all lines in the file

        for line in lines:  # Iterate over each line in the file
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith("states:"):  # Check for states definition
                self.states = set(line.split(":")[1].split(","))  # Extract states and add them to the set
            elif line.startswith("input_symbols:"):  # Check for input symbols definition
                self.input_symbols = set(line.split(":")[1].split(","))  # Extract input symbols
            elif line.startswith("stack_symbols:"):  # Check for stack symbols definition
                self.stack_symbols = set(line.split(":")[1].split(","))  # Extract stack symbols
            elif line.startswith("start_state:"):  # Check for start state definition
                self.start_state = line.split(":")[1].strip()  # Set the start state
            elif line.startswith("accept_states:"):  # Check for accepting states definition
                self.accept_states = set(line.split(":")[1].split(","))  # Extract accepting states
            elif line.startswith("transitions:"):  # Check for transitions header
                continue  # Skip the header line
            elif "->" in line:  # Check if the line defines a transition
                left, right = line.split("->")  # Split the line into left and right parts
                left_parts = left.strip().split()  # Split and process the left part
                right_parts = right.strip().split()  # Split and process the right part

                # Extract transition details
                current_state = left_parts[0]  # Current state
                input_symbol = left_parts[1]  # Input symbol
                stack_top = left_parts[2]  # Top of the stack
                next_state = right_parts[0]  # Next state
                stack_action = right_parts[1] if len(right_parts) > 1 else "e"  # Stack action

                # Add the transition to the dictionary
                self.transitions[(current_state, input_symbol, stack_top)] = (next_state, stack_action)

    def process_string(self, input_string):  # Method to process an input string
        stack = ['']  # Initialize the stack with an empty symbol
        current_state = self.start_state  # Start at the initial state
        steps = []  # List to store processing steps

        for char in input_string:  # Iterate over each character in the input string
            steps.append((current_state, char, ''.join(stack)))  # Record the current state, input, and stack
            found_transition = False  # Flag to check if a valid transition exists

            for (state, symbol, stack_top), (next_state, stack_action) in self.transitions.items():
                # Check if a transition matches the current state, input, and stack top
                if state == current_state and (symbol == char or symbol == "e") and (not stack or stack[-1] == stack_top or stack_top == "e"):
                    found_transition = True  # Valid transition found
                    current_state = next_state  # Update to the next state
                    if stack and stack_top != "e":  # If stack top is not epsilon, pop it
                        stack.pop()
                    if stack_action != "e":  # If stack action is not epsilon, push new symbols
                        stack.extend(reversed(stack_action))  # Push symbols in reverse order
                    break  # Exit the loop once a valid transition is applied

            if not found_transition:  # If no valid transition is found
                steps.append(f"Rejected at state {current_state} with stack {''.join(stack)}")  # Record rejection
                return False, steps  # Return rejection result with steps

        steps.append((current_state, "end", ''.join(stack)))  # Record final state and stack
        # Check if the final state is an accept state and the stack is empty
        if current_state in self.accept_states and stack == ['']:
            return True, steps  # Accept the string
        return False, steps  # Reject the string

if __name__ == "__main__":  # Main execution block
    config_file = "input.txt"  # Specify the configuration file for the automaton
    pda = PushdownAutomaton(config_file)  # Create a PushdownAutomaton object

    input_string = "(2+5)/(3*1)-(1+3-2/4)$"  # Define the input string to process
    accepted, steps = pda.process_string(input_string)  # Process the string and get the result

    print("Processing steps:")  # Output the steps
    for step in steps:  # Iterate over and print each step
        print(step)

    if accepted:  # Check if the string was accepted
        print("The string is accepted by the PDA.")  # Print acceptance message
    else:  # If the string was rejected
        print("The string is rejected by the PDA.")  # Print rejection message
