import json
import os




def simulate_turing_machine(spec_file_content, input_file_content):
    """
    Simulates a single-tape Turing Machine.
    """

    try:
        spec = json.loads(spec_file_content)
    except json.JSONDecodeError:
        return None, "Error: Could not parse JSON specification file.", 0

    initial_state = spec['initial']
    final_states = set(spec['final'])
    blank_symbol = spec['white']
    transitions = {}


    for t in spec['transitions']:
        key = (t['from'], t['read'])
        transitions[key] = (t['to'], t['write'], t['dir'])




    input_string = input_file_content.strip()
    tape = list(input_string)
    head_pos = 0
    current_state = initial_state


    if not tape:
        tape = [blank_symbol]


    def expand_tape(tape, head_pos, blank):
        if head_pos < 0:
            tape.insert(0, blank)
            head_pos = 0
        elif head_pos >= len(tape):
            tape.append(blank)
        return tape, head_pos


    max_steps = 5000
    step_count = 0

    while current_state not in final_states and step_count < max_steps:
        step_count += 1
        tape, head_pos = expand_tape(tape, head_pos, blank_symbol)

        read_symbol = tape[head_pos]

        transition_key = (current_state, read_symbol)

        if transition_key in transitions:
            to_state, write_symbol, direction = transitions[transition_key]


            current_state = to_state


            if direction == 'R':
                head_pos += 1
            elif direction == 'L':
                head_pos -= 1


        else:

            break


    start = 0
    while start < len(tape) and tape[start] == blank_symbol:
        start += 1


    end = len(tape) - 1
    while end >= 0 and tape[end] == blank_symbol:
        end -= 1


    if start <= end:
        final_tape_content = "".join(tape[start:end + 1])
    else:

        final_tape_content = blank_symbol


    if current_state in final_states:
        acceptance_status = 1
        message = f"ACCEPTED (1) - Reached final state {current_state} in {step_count} steps."
    else:
        acceptance_status = 0  # Rejected (halted or ran out of steps)
        if step_count >= max_steps:
            message = f"REJECTED (0) - Exceeded maximum step limit ({max_steps})."
        else:
            message = f"REJECTED (0) - Halted in non-final state {current_state} (No transition defined for reading '{read_symbol}')."

    return final_tape_content, message, acceptance_status




duplo_bal_json_content = """
{
    "initial" : 0,
    "final" : [4],
    "white" : "_",
    "transitions" : [
        {"from": 0, "to": 1, "read": "a", "write": "A", "dir":"R"},
        {"from": 1, "to": 1, "read": "a", "write": "a", "dir":"R"},
        {"from": 1, "to": 1, "read": "B", "write": "B", "dir":"R"},
        {"from": 1, "to": 2, "read": "b", "write": "B", "dir":"L"},
        {"from": 2, "to": 2, "read": "B", "write": "B", "dir":"L"},
        {"from": 2, "to": 2, "read": "a", "write": "a", "dir":"L"},
        {"from": 2, "to": 0, "read": "A", "write": "A", "dir":"R"},
        {"from": 0, "to": 3, "read": "B", "write": "B", "dir":"R"},
        {"from": 3, "to": 3, "read": "B", "write": "B", "dir":"R"},
        {"from": 3, "to": 4, "read": "_", "write": "_", "dir":"L"}      
    ]
}
"""

duplobal_in_content = "aabb"



final_tape, status_message, acceptance_code = simulate_turing_machine(
    duplo_bal_json_content,
    duplobal_in_content
)




print(f"Resultado da Simulação:")
print(f"Código de Aceitação/Rejeição: {acceptance_code} ({'ACEITA' if acceptance_code == 1 else 'REJEITA'})")
print(f"Mensagem: {status_message}")


output_filename = "fita.txt"
with open(output_filename, "w") as f:
    f.write(final_tape)

print(f"Conteúdo final da fita salvo em '{output_filename}':")
print(f"'{final_tape}'")


print(f"\nSaída solicitada na linha de comando: {acceptance_code}")