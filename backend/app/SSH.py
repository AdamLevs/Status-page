import paramiko
import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_server_stats(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)

        commands = {
            "CPU": "top -bn1 | grep 'Cpu(s)'",
            "RAM": "free -m",
            "Disk": "df -h /"
        }

        results = {}
        for key, command in commands.items():
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            results[key] = output

        ssh.close()
        return results

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    host = "192.168.1.100"
    username = "your_user"
    password = "your_password"

    stats = get_server_stats(host, username, password)

    for section, output in stats.items():
        print(f"--- {section} ---")
        print(output)
        print()