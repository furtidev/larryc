from rich.console import Console
from rich.align import Align
from rich.bar import Bar
import requests
import json
import sys
from enum import Enum

class ErrorType(Enum):
	NO_ARG = 1

class App:
	def __init__(self):
		self.console = Console()
		self.color = "green"

	def run(self, word: str):
		request = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
		response = json.loads(request.text)
		try:
			synonyms = response[0]['meanings'][0]['synonyms']
		except KeyError:
			synonyms = []
		if "message" in response:
			self.console.print(f"[red]ERROR:[/red] [green]{response['message']}[/green]")
		else:
			self.console.rule(f"🔍 Viewing Word -> [green]{word.capitalize()}[/green]")
			self.console.print(Align(":book: Definitions", align="center"))
			for i in range(0, len(response[0]['meanings'][0]['definitions'])):
				if self.color == "green":
					self.color = "yellow"
				else:
					self.color = "green"
				self.console.print(f"[{self.color}]• {response[0]['meanings'][0]['definitions'][i]['definition']}[/]", justify="center")
			
			if len(synonyms) != 0:
				self.console.rule("Synoyms")
				for i in synonyms:
					self.console.print(f"[cyan]{i}[/]", justify="center")
			
			
			self.console.rule(f"Made with [b magenta not dim]Rich[/]", characters="~", style="magenta")
			

	def err(self, type: ErrorType):
		if type == ErrorType.NO_ARG:
			self.console.print("[red]USAGE:[/red] [bold green]$ larry <word>[/bold green]")
