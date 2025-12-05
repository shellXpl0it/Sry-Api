# Sry-Api https://discord.gg/pyynMMZfQT

Sry-Api is a powerful and user-friendly command-line tool for managing and interacting with Discord webhooks. Built with Python, it provides a simple, menu-driven interface to check the status of webhooks, send a high volume of messages, and delete them directly from your terminal.

The interface is designed with `rich` to be both beautiful and intuitive.

![Sry-Ping Demo](https://cdn.discordapp.com/attachments/1439272416093143061/1445487698520440943/image.png?ex=693086d3&is=692f3553&hm=e78b64a3eb311f7f00cdf0987352b6225e2e5539970005e9cbac2025b0e52547&)

## About The Project

This tool was created to provide a simple yet effective way to manage Discord webhooks for testing and administrative purposes. It consolidates common webhook actions into one script, saving you the effort of using more complex tools or writing your own scripts for simple tasks.

## Features

*   **Webhook Status Check**: Retrieves and displays detailed information about a given webhook, such as its name, ID, server, and creator.
*   **Webhook Attack**: Sends a specified number of messages to a webhook URL with a configurable delay between each message.
*   **Webhook Wipe**: Permanently deletes a Discord webhook.
*   **Interactive TUI**: A clean and interactive terminal user interface that is easy to navigate.
*   **Cross-Platform**: Works on both Windows and Unix-like systems (Linux, macOS).

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

You need to have Python 3 and `pip` installed on your system.

### Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/shellxpl0it/Sry-Api.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd Sry-Api
    ```
3.  Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the application, run the `main.py` script:

```sh
python main.py
```

You will be greeted by the main menu, where you can select an option by pressing the corresponding number key.

### Function Explanations

*   **1) Status**
    *   This function prompts you for a webhook URL and fetches its current information. If the webhook is valid, it displays details like the webhook name, ID, server ID, channel ID, and creator's username in a clean table format. This is useful for verifying if a webhook is active.

*   **2) Attack**
    *   This function allows you to send a barrage of messages to a specific webhook. It will ask for:
        *   **Webhook URL**: The target for the messages.
        *   **Message**: The content to be sent repeatedly.
        *   **Amount**: The total number of messages to send.
        *   **Delay**: The time (in seconds) to wait between sending each message. A delay of `0` sends messages as fast as possible.

*   **3) Wipe**
    *   This function is used to permanently delete a webhook. It will ask for the webhook URL and require a confirmation before proceeding, as this action is irreversible.

*   **4) Help**
    *   Displays a help menu that provides a brief explanation of each available command.

*   **5) Exit**
    *   Closes the application.

## Disclaimer

This tool is intended for educational and testing purposes only. The "Attack" feature can be disruptive if misused. Please use this tool responsibly and only on webhooks that you own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.

## License

This project is distributed under a proprietary license. Please see the `LICENSE.md` file for more information. In short, you are free to use it for personal, non-commercial purposes, but you may not distribute, modify, or sell it.

---

**Author:** shellxpl0it
