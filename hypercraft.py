import os
import ctypes
import subprocess

class HyperCraft:
    def __init__(self):
        self.powercfg_cmd = "powercfg"
        self.battery_mode = "Battery Saver"
        self.performance_mode = "High Performance"

    def get_current_power_plan(self):
        try:
            output = subprocess.check_output([self.powercfg_cmd, "/getactivescheme"]).decode()
            return output.split('GUID: ')[1].strip().split(' (')[0]
        except Exception as e:
            print(f"Error getting current power plan: {e}")
            return None

    def list_power_plans(self):
        try:
            output = subprocess.check_output([self.powercfg_cmd, "/list"]).decode()
            print("Available Power Plans:")
            print(output)
        except Exception as e:
            print(f"Error listing power plans: {e}")

    def set_power_plan(self, plan_name):
        plan_guid = self.find_power_plan_guid(plan_name)
        if plan_guid:
            try:
                subprocess.call([self.powercfg_cmd, "/setactive", plan_guid])
                print(f"Switched to {plan_name} power plan.")
            except Exception as e:
                print(f"Error setting power plan: {e}")
        else:
            print(f"Power plan '{plan_name}' not found.")

    def find_power_plan_guid(self, plan_name):
        try:
            output = subprocess.check_output([self.powercfg_cmd, "/list"]).decode()
            plans = output.split('\n')
            for plan in plans:
                if plan_name.lower() in plan.lower():
                    return plan.split('GUID: ')[1].strip().split('  (')[0]
        except Exception as e:
            print(f"Error finding power plan GUID: {e}")
        return None

    def set_battery_saver(self):
        self.set_power_plan(self.battery_mode)

    def set_performance_mode(self):
        self.set_power_plan(self.performance_mode)

    def optimize_settings(self):
        print("Optimizing settings for battery life...")
        # Example settings adjustments
        os.system("powercfg /change monitor-timeout-dc 5")
        os.system("powercfg /change standby-timeout-dc 10")
        os.system("powercfg /change hibernate-timeout-dc 15")
        print("Settings optimized for extended battery life.")

    def run(self):
        current_plan = self.get_current_power_plan()
        if current_plan:
            print(f"Current Power Plan GUID: {current_plan}")
        self.list_power_plans()

        user_choice = input("Choose mode: [1] Battery Saver [2] Performance [3] Optimize: ")
        if user_choice == '1':
            self.set_battery_saver()
        elif user_choice == '2':
            self.set_performance_mode()
        elif user_choice == '3':
            self.optimize_settings()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    hypercraft = HyperCraft()
    hypercraft.run()