import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json 
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Simulate capacitor charging and discharging with checkpointing.")

    parser.add_argument("--cap", type=str, default="220e-6", help="Comma-separated capacitance values in farads (default: '220e-6')")
    parser.add_argument("--r_charging", type=float, default=1000, help="Resistance during charging in ohms (default: 1000 Ω)")
    parser.add_argument("--v_start", type=float, default=3.3, help="Startup voltage of MCU (default: 3.3 V)")
    parser.add_argument("--v_cutoff", type=float, default=1.8, help="Minimum operating voltage of MCU (default: 1.8 V)")
    parser.add_argument("--total_cycles_required", type=int, default=100000, help="Total cycles required by the application (default: 100000 cycles)")
    parser.add_argument("--total_checkpoint_size", type=int, default=128, help="Total bytes required by the checkpoint in bytes (default: 128 bytes)")
    parser.add_argument("--total_restore_size", type=int, default=128, help="Total bytes required by the restore in bytes (default: 128 bytes)")
    parser.add_argument("--trace", type=str, default='traces/RF_2.csv', help="CSV file path for voltage values (default: '\traces\RF_2.csv')")
    parser.add_argument("--mcu", type=str, default="stm32l152re_32Mhz", help="MCU name for the experiment (e.g., stm32l152re_32Mhz)")
    parser.add_argument("--g", action='store_true', help="Generate graphs if this flag is set")
    parser.add_argument("-j", "--json", action='store_true', help="Output results in JSON format if this flag is set")

    return parser.parse_args()

args = parse_args()

# Read MCU parameters from mcu.csv
mcu_df = pd.read_csv('mcu.csv')
mcu_params = mcu_df[mcu_df['name'] == args.mcu].iloc[0]

# Extract MCU parameters
R_discharging = mcu_params['effective_resistance']
energy_per_cycle = mcu_params['energy_per_cycle']
write_energy_per_byte = mcu_params['write_energy_per_byte']
read_energy_per_byte = mcu_params['read_energy_per_byte']

# Parse capacitance values
capacitance_values = [float(c) for c in args.cap.split(',')]

# Common parameters
R_charging = args.r_charging
V_discharge_start = args.v_start
V_cutoff = args.v_cutoff
total_cycles_required = args.total_cycles_required
total_checkpoint_energy = args.total_checkpoint_size * write_energy_per_byte
total_restore_energy = args.total_restore_size * read_energy_per_byte
csv_file = args.trace

v_max_values_df = pd.read_csv(csv_file, header=None)
V_max_values = v_max_values_df[0].values  # Assuming the values are in the first column

# Time array based on the number of V_max values, with each step representing 1 millisecond
time = np.arange(len(V_max_values)) / 1000  # Divide by 1000 to convert milliseconds to seconds

# Function to simulate and print results for each capacitor size
def simulate_for_capacitor(C):
    voltage = np.zeros(len(time))

    # Initial conditions
    charging = True
    V = 0  # initial voltage
    t_charge_start = 0  # time when the last charging started
    t_discharge_start = 0  # time when the last discharging started
    total_energy_consumed = 0  # Variable to store total energy consumed
    checkpoint_count = 0  # Counter for the number of checkpoints
    V_initial = 0  # initial voltage of the capacitor
    V_check_thres = np.sqrt(2 * (total_checkpoint_energy + (0.5 * C * V_cutoff**2)) / C)  # checkpoint voltage threshold
    charging_states = []
    energy_discharge_event_occurred = False

    for i, t in enumerate(time):
        V_max = V_max_values[i]  # Use the Voltage Trace

        if charging:
            # Calculate voltage during charging
            if V_max > V:
                V = V_initial + (V_max - V_initial) * (1 - np.exp(-(0.001) / (R_charging * C)))
                V_initial = V
            if V >= V_discharge_start:
                # Start discharging
                charging = False
                t_discharge_start = t
                V_initial = V
                E_initial = 0.5 * C * V_initial ** 2  # Energy at the start of discharge
                energy_discharge_event_occurred = False  # Reset the flag at the beginning of discharge
        else:
            # Calculate voltage during discharging
            V = V_initial * np.exp(-(0.001) / (R_discharging * C))
            V = V + (V_max - V) * (1 - np.exp(-(0.001) / (R_charging * C)))
            V_initial = V

            # Check if energy discharged reaches checkpoint location
            if V <= V_check_thres and not energy_discharge_event_occurred:
                charging_states.append(t)  # Record time slightly before the new charge cycle
                energy_discharge_event_occurred = True  # Set the flag to prevent multiple recordings

            if V <= V_cutoff:
                # Start charging
                charging = True
                E_final = 0.5 * C * V_initial ** 2  # Energy at the end of discharge
                total_energy_consumed += E_initial - E_final - total_checkpoint_energy - total_restore_energy
                if total_energy_consumed < 0:
                    print(f"Checkpointing not possible for C = {C} F")
                    break
                if total_energy_consumed >= total_cycles_required * energy_per_cycle:
                    break
                t_charge_start = t
                V_initial = V
                checkpoint_count += 1  # Increment the discharge cycle counter

        voltage[i] = V

    if args.json:
        results = {
            "Capacitance": float(C),  # Ensure C is a standard Python float
            "Checkpointing Voltage Threshold": float(V_check_thres),  # Convert to float
            "Total energy consumed": float(total_energy_consumed),  # Convert to float
            "Total energy required": float(total_cycles_required * energy_per_cycle),  # Convert to float
            "Total number of checkpoints": int(checkpoint_count) if total_energy_consumed >= total_cycles_required * energy_per_cycle else "N/A",
            "Execution completed": bool(total_energy_consumed >= total_cycles_required * energy_per_cycle)  # Convert to bool
        }
        print(json.dumps(results, indent=4))
    else:
        print(f"Results for Capacitance: {C} F")
        print(f"Checkpointing Voltage Threshold: {V_check_thres} V")
        print(f"Total energy consumed: {total_energy_consumed} Joules")
        print(f"Total energy required: {total_cycles_required * energy_per_cycle} Joules")
        if total_energy_consumed >= total_cycles_required * energy_per_cycle:
            print(f"Total number of checkpoints: {checkpoint_count}")
        else:
            print("Application execution not completed")
        print("-------")

    # Plotting the graph only if --g flag is set
    if args.g:
        plt.figure(figsize=(12, 2.5))
        plt.plot(time[:i+1], V_max_values[:i+1], label='Voltage Trace', color='#B9B9B9', linestyle='--')  # Plot up to the break point
        plt.plot(time[:i+1], voltage[:i+1], label=f'Capacitor Voltage (C = {C} F)', color='#000000')  # Plot up to the break point

        # Adding vertical lines for V_discharge_start and V_cutoff
        plt.axhline(y=V_discharge_start, color='#48A300', linestyle='dotted')
        plt.axhline(y=V_cutoff, color='#B82100', linestyle='dotted')
        plt.axhline(y=V_check_thres, color='#B748FF', linestyle='dotted')

        # Adding text labels for the lines
        plt.text(x=0.1, y=V_discharge_start + 0.04, s='Startup Voltage', color='black', verticalalignment='bottom', fontsize=8)
        plt.text(x=0.1, y=V_cutoff - 0.5, s='Minimum Operating Voltage', color='black', verticalalignment='bottom', fontsize=8)
        plt.text(x=0.1, y=V_check_thres - 0.5, s='Checkpointing Threshold', color='black', verticalalignment='bottom', fontsize=8)

        # Adding orange vertical lines at each discharge point
        label_added = False
        for idx, t in enumerate(charging_states):
            if not label_added:
                plt.axvline(x=t, color='#F07100', linestyle='--', linewidth=1, label='Checkpoint Location')
                plt.text(x=t, y=plt.ylim()[1] * -0.08, s=str(idx + 1), color='black', verticalalignment='top',
                     horizontalalignment='center', fontsize=8)
                label_added = True
            else:
                plt.axvline(x=t, color='#F07100', linestyle='--', linewidth=1)
                plt.text(x=t, y=plt.ylim()[1] * -0.08, s=str(idx + 1), color='black', verticalalignment='top',
                     horizontalalignment='center', fontsize=8)

        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.grid(True, axis='x')  # Enable only vertical gridlines
        plt.legend()
        plt.tight_layout()
        plt.show()

# Run simulation for each capacitance value
for C in capacitance_values:
    simulate_for_capacitor(C)
