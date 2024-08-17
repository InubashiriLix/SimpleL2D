# Live2D Sound-Activated Image Display

# 基于声音激活的Live2D图像显示

This project is a PySide6-based application that displays images depending on the presence of external sound input. For instance, when sound is detected (e.g., when someone is speaking), an "active" image is displayed, and when no sound is detected, a "silent" image is shown.

这个项目是一个基于 PySide6 的应用程序，根据外部声音输入显示图像。例如，当检测到声音时（例如有人讲话时），显示“激活”图像；当没有声音时，显示“静默”图像。

## Table of Contents
 
## 目录

- [Workflow](#workflow) | [工作流程](#工作流程)
- [How It Works](#how-it-works) | [工作原理](#工作原理)
- [Features](#features) | [功能](#功能)
- [Setup and Installation](#setup-and-installation) | [安装与设置](#安装与设置)
- [Usage](#usage) | [使用方法](#使用方法)
- [To-Do List](#to-do-list) | [待办事项](#待办事项)
- [Contributing](#contributing) | [贡献](#贡献)

## Workflow

## 工作流程

1. **Configuration**:
    - The user is prompted to select images for both "active" (when sound is detected) and "silent" (when no sound is detected) states.
    - A sound threshold (in dB) is configured to determine the sensitivity of the sound detection.
    - Configuration settings are saved to a `config.json` file for future use.

1. **配置**：
    - 用户需要选择“激活”（检测到声音时）和“静默”（没有声音时）状态的图像。
    - 配置声音阈值（以 dB 为单位）来确定声音检测的灵敏度。
    - 配置设置会保存到 `config.json` 文件中以供日后使用。

2. **Sound Detection**:
    - A sound stream is initiated using the `sounddevice` library, and the sound input is continuously monitored.
    - The Root Mean Square (RMS) of the audio input is calculated and converted into decibels (dB).
    - If the sound level exceeds the configured threshold, the active image is displayed; otherwise, the silent image is shown.

2. **声音检测**：
    - 使用 `sounddevice` 库启动声音流，持续监测声音输入。
    - 计算音频输入的均方根值 (RMS) 并转换为分贝 (dB)。
    - 如果声音水平超过配置的阈值，则显示激活图像；否则显示静默图像。

3. **Image Display**:
    - The `Live2D` window displays either the active or silent image based on the sound detection results.
    - The window is frameless, always stays on top, and allows for custom context menus for easy interaction (e.g., exiting the application).

3. **图像显示**：
    - `Live2D` 窗口根据声音检测结果显示激活或静默图像。
    - 窗口无边框，总是保持在最上方，并允许自定义上下文菜单以便于交互（例如退出应用程序）。

4. **Main Window**:
    - The application starts with a main window where users can configure settings or start the Live2D image display.
    - The main window hides itself when the Live2D window is active and reappears when the Live2D window is closed.

4. **主窗口**：
    - 应用程序以主窗口启动，用户可以在其中配置设置或启动 Live2D 图像显示。
    - 当 Live2D 窗口处于活动状态时，主窗口隐藏；当 Live2D 窗口关闭时，主窗口重新显示。

## How It Works

## 工作原理

- **Sound Detection**:
  - The `sounddevice` library is used to capture audio input from the microphone.
  - The RMS of the input audio is calculated, converted to dB, and compared against a user-defined threshold.

- **声音检测**：
  - 使用 `sounddevice` 库捕获来自麦克风的音频输入。
  - 计算输入音频的 RMS 值，将其转换为 dB，并与用户定义的阈值进行比较。

- **Image Switching**:
  - Depending on the detected sound level, the `Live2D` window switches between the active and silent images.

- **图像切换**：
  - 根据检测到的声音水平，`Live2D` 窗口在激活和静默图像之间切换。

- **Configuration Management**:
  - Configuration settings (image paths and sound threshold) are stored in a `config.json` file. These settings can be modified through the main window's configuration options.

- **配置管理**：
  - 配置设置（图像路径和声音阈值）存储在 `config.json` 文件中。用户可以通过主窗口的配置选项修改这些设置。

## Features

## 功能

- **Customizable Images**: Users can select their own images for active and silent states.
- **Sound Sensitivity Control**: Users can define the sound threshold that triggers the image switch.
- **Frameless Floating Window**: The Live2D window is a transparent, frameless floating window that stays on top of other windows.
- **Context Menu**: A context menu allows users to exit the Live2D window easily.

- **自定义图像**：用户可以为激活和静默状态选择自己的图像。
- **声音灵敏度控制**：用户可以定义触发图像切换的声音阈值。
- **无边框浮动窗口**：Live2D 窗口是透明的无边框浮动窗口，总是保持在其他窗口的最上方。
- **上下文菜单**：上下文菜单允许用户轻松退出 Live2D 窗口。

## Setup and Installation

## 安装与设置

1. **Install Dependencies**:
   - Ensure you have Python installed, then install the required dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - `requirements.txt` should include:
     ```plaintext
     PySide6
     sounddevice
     numpy
     pyaudio
     ```

1. **安装依赖**：
   - 确保你已安装 Python，然后安装所需的依赖：

     ```bash
     pip install -r requirements.txt
     ```

   - `requirements.txt` 文件应包含：
     ```plaintext
     PySide6
     sounddevice
     numpy
     pyaudio
     ```

2. **Run the Application**:
   - Start the application by running the following command:

     ```bash
     python live2d.py
     ```

2. **运行应用程序**：
   - 通过以下命令启动应用程序：

     ```bash
     python live2d.py
     ```

## Usage

## 使用方法

1. **Configuration**:
   - On the main window, click "Config" to configure the active and silent images and set the sound threshold.

1. **配置**：
   - 在主窗口中，点击“Config”配置激活和静默图像，并设置声音阈值。

2. **Start Live2D**:
   - After configuration, click "Start" to launch the Live2D window. The window will now display images based on detected sound.

2. **启动 Live2D**：
   - 配置完成后，点击“Start”启动 Live2D 窗口。窗口现在将根据检测到的声音显示图像。

3. **Interact with Live2D Window**:
   - Right-click to open the context menu and select "Exit" to close the Live2D window.

3. **与 Live2D 窗口交互**：
   - 右键点击以打开上下文菜单，选择“Exit”关闭 Live2D 窗口。

## To-Do List

## 待办事项

- **Support Custom Window Sizes**:
  - Add functionality to allow users to set custom window sizes, rather than relying on the original image dimensions.

- **支持自定义窗口大小**：
  - 添加功能以允许用户设置自定义窗口大小，而不是依赖于原始图像尺寸。

- **Code Optimization**:
  - Refactor and optimize the code for better performance, particularly in the areas of sound processing and image switching.

- **代码优化**：
  - 重构和优化代码以提高性能，特别是在声音处理和图像切换方面。

- **Support More Image Formats**:
  - Extend support to additional image formats, including GIFs, to allow for animated images.

- **支持更多图像格式**：
  - 扩展对其他图像格式的支持，包括 GIF，以允许显示动画图像。

## Contributing

## 贡献

Contributions to the project are welcome! Please fork the repository, create a feature branch, and submit a pull request with your changes.

欢迎对该项目做出贡献！请 fork 此仓库，创建一个功能分支，并提交包含您更改的 pull request。

- **Reporting Issues**:
  - If you find bugs or have suggestions, feel free to open an issue in the repository.

- **报告问题**：
  - 如果你发现了错误或有建议，请随时在仓库中提交一个 issue。

- **Pull Requests**:
  - Ensure your code adheres to the project's coding standards and includes tests for new features.

- **提交 Pull Request**：
  - 确保你的代码符合项目的编码标准，并为新功能包含测试。

## License

## 许可

This project is licensed under the MIT License. See the LICENSE file for more details.

该项目使用 MIT 许可证。详情请参阅 LICENSE 文件。

---
