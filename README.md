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
- `--mcu`: MCU name for the experiment (e.g., `stm32l152re`). Default: `"stm32l152re"`.
- `--g`: Generate graphs if this flag is set.

### Example Command

```sh
python capacitor_simulation.py --cap "220e-6,470e-6" --r_charging 1000 --v_start 3.3 --v_cutoff 1.8 --total_cycles_required 100000 --total_checkpoint_size 128 --total_restore_size 128 --trace 'RF_2.csv' --mcu 'stm32l152re' --g
```


## Expected Output

   The script will output the results for each capacitor value provided:

   ```
   Results for Capacitance: 2.2e-05 F
   Checkpointing Voltage Threshold: 0.014340325153947708 V
   Total energy consumed: 0.002825661846 Joules
   Total energy required: 0.002825661846 Joules
   Total number of checkpoints: 10
   ------
   Results for Capacitance: 4.7e-05 F
   Checkpointing Voltage Threshold: 0.010123234424095573 V
   Total energy consumed: 0.004325661846 Joules
   Total energy required: 0.004325661846 Joules
   Total number of checkpoints: 15
   ```

   If the `--g` flag is set, graphs will be generated for each capacitor value, showing the voltage traces and capacitor voltage.

   ![Alt text](/docs/screenshots/Figure_1.png?raw=true "Optional Title")
   ![Alt text](/docs/screenshots/Figure_2.png?raw=true "Optional Title")

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
