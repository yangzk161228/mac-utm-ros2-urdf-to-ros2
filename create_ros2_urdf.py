import os
import re
import shutil
import subprocess

def print_colored(command, description, color_code):
    """Print command and description with specified ANSI color."""
    print(f"\033[{color_code}m{description}: \033[1;37m{command}\033[0m")

def replace_in_file(file_path, old_str, new_str):
    """Replace a substring in a file with a new substring."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = file.read()
        filedata = filedata.replace(old_str, new_str)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(filedata)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def git_clone_urdf(src_dir):
    """Clone the URDF lesson repository if it does not exist."""
    lesson_urdf_path = os.path.join(src_dir, 'lesson_urdf')
    if not os.path.exists(lesson_urdf_path):
        print_colored(f"The 'lesson_urdf' directory does not exist in {src_dir}.", "Check", 93)  # Yellow
        response = input("Do you want to clone the 'lesson_urdf' from GitHub? (y/n): ").strip().lower()
        if response == 'y':
            try:
                subprocess.run(["git", "clone", "https://github.com/olmerg/lesson_urdf.git", lesson_urdf_path], check=True)
                print_colored(f"Successfully cloned 'lesson_urdf' into {src_dir}.", "Success", 92)  # Green
                return True
            except subprocess.CalledProcessError:
                print_colored("Failed to clone 'lesson_urdf'.", "Error", 91)  # Red
        else:
            print_colored("Operation cancelled.", "Status", 91)  # Red
        return False
    return True

def copy_urdf_files(src_dir, project_name):
    """Copy URDF related directories and files to the new project."""
    source_path = os.path.join(src_dir, 'lesson_urdf')
    target_path = os.path.join(src_dir, project_name)
    for folder in ['launch', 'meshes', 'rviz', 'urdf']:
        shutil.copytree(os.path.join(source_path, folder), os.path.join(target_path, folder), dirs_exist_ok=True)
    print_colored("URDF environment setup is complete.", "Setup Complete", 92)  # Green
    
    # Copy and replace contents in setup.py and package.xml
    for file_name in ['setup.py', 'package.xml']:
        source_file = os.path.join(source_path, file_name)
        target_file = os.path.join(target_path, file_name)
        if os.path.exists(source_file):
            shutil.copy(source_file, target_file)
            replace_in_file(target_file, 'lesson_urdf', project_name)
            print_colored(f"Copied and modified {file_name}.", "File Operation", 92)  # Green
        else:
            print_colored(f"Source file not found: {source_file}", "Error", 91)  # Red
            
def import_model_files(src_dir, project_name):
    """Import model files specified by the user."""

    while True:
        model_dir = input("Please input urdf model directory：")
        visual_dir = os.path.join(src_dir, project_name, 'meshes', 'visual')
        urdf_dir = os.path.join(src_dir, project_name, 'urdf')

        if os.path.exists(model_dir):
            if os.path.exists(os.path.join(model_dir, "meshes")):
                if os.path.exists(visual_dir):
                    shutil.rmtree(visual_dir)

                os.makedirs(visual_dir)
                break
        else:
            print_colored("directory incorrect, inputed path not include meshes directory。", 'Error', 91)
        
    # Copy all files from the model's meshes directory
    model_meshes_dir = os.path.join(model_dir, 'meshes')
    if os.path.exists(model_meshes_dir):
        for file_name in os.listdir(model_meshes_dir):
            source_file = os.path.join(model_meshes_dir, file_name)
            target_file = os.path.join(visual_dir, file_name)
            shutil.copy(source_file, target_file)
        print_colored("Model files imported successfully to visual directory.", "Success", 92)
    else:
        print_colored("Model meshes directory not found.", "Error", 91)
        
    # Copy all files from the model's urdf directory
    model_urdf_dir = os.path.join(model_dir, 'urdf')
    if os.path.exists(model_urdf_dir):
        for file_name in os.listdir(model_urdf_dir):
            source_file = os.path.join(model_urdf_dir, file_name)
            target_file = os.path.join(urdf_dir, file_name)
            shutil.copy(source_file, target_file)
        print_colored("Model files imported successfully to visual directory.", "Success", 92)
    else:
        print_colored("Model urdf directory not found.", "Error", 91)

        
def update_urdf_configuration(src_dir, project_name):
    urdf_dir = os.path.join(src_dir, project_name, 'urdf')
    # 获取所有的.urdf文件
    urdf_files = [f for f in os.listdir(urdf_dir) if f.endswith('.urdf')]
    if len(urdf_files) == 0:
        print_colored("Directory not include *.urdf file.", 'Error', 91)
        return
    elif len(urdf_files) == 1:
        selected_urdf = urdf_files[0]
    else:
        print_colored(".urdf files find as below list:", "Success", 92)
        for i, urdf_file in enumerate(urdf_files):
            print(f"{i + 1}. {urdf_file}")
        
        while True:
            try:
                choice = int(input("Please select code to use URDF file."))
                if 1 <= choice <= len(urdf_files):
                    selected_urdf = urdf_files[choice - 1]
                    break
                else:
                    print_colored("Please input correct code.", 'Warning', 93)
            except ValueError:
                print("请输入一个整数编号。")
                print_colored("Please input an integer.", 'Error', 91)
    
    print_colored(f" {selected_urdf} was selected.", "Success", 92)
    
    # 删除其他URDF文件
    for file in urdf_files:
        if file != selected_urdf:
            os.remove(os.path.join(urdf_dir, file))
    
    # 重命名选定的URDF文件为项目名称
    new_urdf_name = f"{project_name}.urdf"
    os.rename(os.path.join(urdf_dir, selected_urdf), os.path.join(urdf_dir, new_urdf_name))
    print_colored(f"Change {selected_urdf} name to {new_urdf_name} success.", "Success", 92)

    # 读取选定的URDF文件
    urdf_path = os.path.join(urdf_dir, new_urdf_name)
    with open(urdf_path, 'r') as file:
        urdf_content = file.read()
    
    # 使用正则表达式进行更改
    urdf_content = re.sub(r'<robot(\s*)name="(.+?)"(\s*)>', rf'<robot \1name="{project_name}"\3>', urdf_content)
    urdf_content = re.sub(r'/meshes/', '/meshes/visual/', urdf_content)
    urdf_content = re.sub(r'(\s*)filename(\s*)=(\s*)"package://([^/]+)/',
                          rf'\1filename="package://{project_name}/', urdf_content)

    
    # 写入更改后的内容
    with open(urdf_path, 'w') as file:
        file.write(urdf_content)

    print_colored(f"Update {new_urdf_name} success.", "Success", 92)


def update_launch_configuration(src_dir, project_name):
    launch_dir = os.path.join(src_dir, project_name, 'launch')

    # 读取选定的URDF文件
    launch_file_path = os.path.join(launch_dir, 'view_robot_launch.py')
    with open(launch_file_path, 'r') as file:
        content = file.read()

    # 使用正则表达式进行更改
    content = re.sub(r'lesson_urdf', rf'{project_name}', content)
    content = re.sub(r'planar_3dof', rf'{project_name}', content)
    # 写入更改后的内容
    with open(launch_file_path, 'w') as file:
        file.write(content)

    print_colored(f"Update view_robot_launch.py success.", "Success", 92)

def update_rviz_configuration(src_dir, project_name):
    launch_dir = os.path.join(src_dir, project_name, 'rviz')

    file_path = os.path.join(launch_dir, 'view.rviz')
    with open(file_path, 'r') as file:
        content = file.read()

    # 使用正则表达式进行更改
    content = re.sub(r'world', r'base_link', content)
    # 写入更改后的内容
    with open(file_path, 'w') as file:
        file.write(content)

    print_colored(f"Update view.rviz success.", "Success", 92)


def start_up_ros(src_dir, project_name):
    print_colored(f"--------------Start Building------------------", "Warning", 93)
    subprocess.run(["colcon", "build", "--packages-select", project_name, "--allow-overriding", project_name ], check=True)
    print_colored(f"--------------Building Complete------------------", "Success", 92)

    # print("当前所在目录：", os.getcwd())

    print_colored(f"--------------Start Ros2------------------", "Warning", 93)
    # 设置环境变量
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(src_dir, project_name, "install", "lib", "python3", "dist-packages") + ":" + env.get("PYTHONPATH", "")
    env["LD_LIBRARY_PATH"] = os.path.join(src_dir, project_name, "install", "lib") + ":" + env.get("LD_LIBRARY_PATH", "")

    # 进入工作目录
    os.chdir(os.path.join(src_dir, project_name))

    # 启动 ros2 launch
    subprocess.run(["ros2", "launch", project_name, "view_robot_launch.py"], check=True, env=env)


def create_ros2_package():
    project_name = input("Please enter the project name: ")
    current_dir = os.getcwd()
    src_dir = os.path.join(current_dir, 'src')  # Define src directory path
    project_path = os.path.join(src_dir, project_name)  # Define full project path

    if not os.path.exists(src_dir):
        os.makedirs(src_dir)
        print_colored(f"mkdir -p {src_dir}", "Creating directory", 93)  # Yellow

    if os.path.exists(project_path):
        response = input(f"The project '{project_name}' already exists at '{src_dir}'. Do you want to delete and recreate it? (y/n): ").strip().lower()
        while response not in ['y', 'n']:
            response = input("Please enter 'y' or 'n': ").strip().lower()
        if response == 'n':
            print_colored("Operation cancelled.", "Status", 91)  # Red
            return
        else:
            shutil.rmtree(project_path)
            print_colored(f"rm -rf {project_path}", "Deleting project", 91)  # Red

    subprocess.run(["ros2", "pkg", "create", project_name, "--build-type", "ament_python", "--destination-directory", src_dir], check=True)
    print_colored(f"The ROS 2 package '{project_name}' has been successfully created at '{src_dir}'.", "Success", 92)  # Green

    response = input("Do you want to import and convert URDF files? (y/n): ").strip().lower()
    if response == 'y':
        if git_clone_urdf(src_dir):
            copy_urdf_files(src_dir, project_name)
            import_model_files(src_dir, project_name)
            update_urdf_configuration(src_dir, project_name)
            update_launch_configuration(src_dir, project_name)
            update_rviz_configuration(src_dir, project_name)
            start_up_ros(src_dir, project_name)

if __name__ == "__main__":
    create_ros2_package()

