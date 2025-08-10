#!/usr/bin/env python3

import sys
import paramiko
import winrm

def detect_os(host, username, password, port):
    if port == "22":  # SSH (Linux/macOS)
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=username, password=password, timeout=5)

            # Try standard ways to get OS name + version
            commands = [
                "cat /etc/os-release",  # most modern Linux distros
                "lsb_release -a",       # alternative Linux info
                "sw_vers"               # macOS version info
            ]

            full_output = ""
            for cmd in commands:
                try:
                    stdin, stdout, stderr = client.exec_command(cmd)
                    output = stdout.read().decode().strip()
                    if output:
                        full_output = output
                        break
                except Exception:
                    continue

            client.close()

            if not full_output:
                print("unknown")
                return

            # Parse output for common OS/version indicators
            if "ubuntu" in full_output.lower():
                for line in full_output.splitlines():
                    if line.startswith("PRETTY_NAME="):
                        print(line.split("=")[1].strip('"'))
                        return
            elif "centos" in full_output.lower() or "red hat" in full_output.lower():
                for line in full_output.splitlines():
                    if line.startswith("PRETTY_NAME="):
                        print(line.split("=")[1].strip('"'))
                        return
            elif "macos" in full_output.lower() or "sw_vers" in full_output.lower():
                version = ""
                product = ""
                for line in full_output.splitlines():
                    if "ProductName" in line:
                        product = line.split(":")[1].strip()
                    elif "ProductVersion" in line:
                        version = line.split(":")[1].strip()
                print(f"{product} {version}")
                return
            else:
                print(full_output.splitlines()[0])
                return

        except Exception as e:
            print("error", file=sys.stderr)
            sys.exit(1)

    elif port == "5985":  # WinRM (Windows)
        try:
            session = winrm.Session(f'http://{host}:5985/wsman', auth=(username, password))
            result = session.run_cmd('systeminfo')

            output = result.std_out.decode().lower()

            if "os name" in output and "os version" in output:
                lines = output.splitlines()
                os_name = ""
                os_version = ""

                for line in lines:
                    if "os name" in line:
                        os_name = line.split(":", 1)[1].strip()
                    elif "os version" in line:
                        os_version = line.split(":", 1)[1].strip()
                        break

                print(f"{os_name} {os_version}")
                return
            else:
                print("windows (unknown version)")
                return

        except Exception as e:
            print("error", file=sys.stderr)
            sys.exit(1)

    else:
        print("unsupported", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: detect_os.py <host> <username> <password> <port>")
        sys.exit(1)

    host = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    port = sys.argv[4]

    detect_os(host, username, password, port)

