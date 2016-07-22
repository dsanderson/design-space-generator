import subprocess

if __name__ == '__main__':
    #launch the generator in the background
    subprocess.Popen(["python", "generator.py"])
    #launch the REST API server in the foreground, and pipe output through
    subprocess.call(["python", "server.py"])
