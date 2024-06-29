# CapSimu
Capacitor Charging and Discharging Simulation for intermittent checkpointing systems

## Purpose

This script simulates the charging and discharging process of a capacitor, considering various parameters such as the MCU (Microcontroller Unit) properties, capacitor size, and energy requirements. The simulation helps determine the feasibility of checkpointing in systems powered by intermittent energy sources.

### Equations Used

1. **Charging Voltage:**
  $$V = V_{\text{initial}} + (V_{\text{max}} - V_{\text{initial}}) \cdot \left(1 - \exp\left(\frac{-0.001}{R_{\text{charging}} \cdot C}\right)\right)$$

2. **Discharging Voltage:**
   $$V = V_{\text{initial}} \cdot \exp\left(\frac{-0.001}{R_{\text{discharging}} \cdot C}\right)$$
   $$V = V + (V_{\text{max}} - V) \cdot \left(1 - \exp\left(\frac{-0.001}{R_{\text{charging}} \cdot C}\right)\right)$$

## Usage

### Command-Line Arguments

- `--cap`: Comma-separated capacitance values in farads (e.g., "220e-6,330e-6,470e-6"). Default: `"220e-6"`.
- `--r_charging`: Resistance during charging in ohms. Default: `1000`.
- `--v_start`: Startup voltage of MCU. Default: `3.3`.
- `--v_cutoff`: Minimum operating voltage of MCU. Default: `1.8`.
- `--total_cycles_required`: Total cycles required by the application. Default: `100000`.
- `--total_checkpoint_size`: Total bytes required by the checkpoint in bytes. Default: `128`.
- `--total_restore_size`: Total bytes required by the restore in bytes. Default: `128`.
- `--trace`: CSV file path for voltage values. Default: `'RF_2.csv'`.
- `--mcu`: MCU name for the experiment (e.g., `stm32l152re_32Mhz`). Default: `"stm32l152re_32Mhz"`.
- `--g`: Generate graphs if this flag is set.

### Example Command

```sh
python capsimu.py --cap "220e-6,330e-6,470e-6" --r_charging 1000 --v_start 3.3 --v_cutoff 1.8 --total_cycles_required 100000 --total_checkpoint_size 128 --total_restore_size 128 --trace '/traces/RF_2.csv' --mcu 'stm32l152re_32Mhz' --g
```


## Expected Output

   The script will output the results for each capacitor value provided:

   ```
Results for Capacitance: 0.00022 F
Checkpointing Voltage Threshold: 3.285897137769227 V
Total energy consumed: 6.785915860118819e-05 Joules
Total energy required: 6.43125e-05 Joules
Total number of checkpoints: 4
-------
Results for Capacitance: 0.00033 F
Checkpointing Voltage Threshold: 2.8771652715824305 V
Total energy consumed: 0.00043187257008001827 Joules
Total energy required: 6.43125e-05 Joules
Total number of checkpoints: 0
-------
Results for Capacitance: 0.00047 F
Checkpointing Voltage Threshold: 2.6033392631673915 V
Total energy consumed: 0.000969807619464742 Joules
Total energy required: 6.43125e-05 Joules
Total number of checkpoints: 0
-------
   ```

   If the `--g` flag is set, graphs will be generated for each capacitor value, showing the voltage traces and capacitor voltage.

   ![Alt text](/docs/screenshots/Figure_1.png?raw=true "Optional Title")
   ![Alt text](/docs/screenshots/Figure_2.png?raw=true "Optional Title")
   ![Alt text](/docs/screenshots/Figure_3.png?raw=true "Optional Title")


Here’s a sample documentation section for your GitHub repository that describes the `--json` flag, along with the example input command and the expected JSON output format. You can include this in your README or documentation file to help users understand how to use this feature.

---

## JSON Output Feature

The `--json` flag enables the output of simulation results in JSON format. This can be particularly useful for integrating these results into data analysis pipelines or when automating multiple simulations for batch processing.

### Usage

To enable JSON output, add the `--json` flag at the end of your command line arguments when running the simulation. Below is an example command with multiple configurations:

```bash
python capsimu.py --cap "220e-6,330e-6,470e-6" --r_charging 1000 --v_start 3.3 --v_cutoff 1.8 --total_cycles_required 100000 --total_checkpoint_size 128 --total_restore_size 128 --trace '/traces/RF_2.csv' --mcu 'stm32l152re_32Mhz' --json
```

### Expected JSON Output

The JSON output format provides detailed results for each capacitor size specified in the `--cap` argument. Each block of JSON data includes:

- **Capacitance**: The capacitance value used in the simulation.
- **Checkpointing Voltage Threshold**: The calculated voltage threshold for checkpointing.
- **Total energy consumed**: The total energy consumed during the simulation.
- **Total energy required**: The total energy requirement calculated based on the number of cycles and per cycle energy consumption.
- **Total number of checkpoints**: The number of checkpoints that occurred during the simulation.
- **Execution completed**: A boolean indicating whether the application execution requirements were met.

### Example Output

```json
{
    "Capacitance": 0.00022,
    "Checkpointing Voltage Threshold": 3.285897137769227,
    "Total energy consumed": 6.785915860118819e-05,
    "Total energy required": 6.43125e-05,
    "Total number of checkpoints": 4,
    "Execution completed": true
}
{
    "Capacitance": 0.00033,
    "Checkpointing Voltage Threshold": 2.8771652715824305,
    "Total energy consumed": 0.00043187257008001827,
    "Total energy required": 6.43125e-05,
    "Total number of checkpoints": 0,
    "Execution completed": true
}
{
    "Capacitance": 0.00047,
    "Checkpointing Voltage Threshold": 2.6033392631673915,
    "Total energy consumed": 0.000969807619464742,
    "Total energy required": 6.43125e-05,
    "Total number of checkpoints": 0,
    "Execution completed": true
}
```

This output is ideal for logging, automated parsing, or for use in subsequent automated systems. Ensure that your runtime environment supports Python's JSON capabilities to utilize this feature effectively.

---


## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
