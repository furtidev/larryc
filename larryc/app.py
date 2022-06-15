'''
The command-line parser for the package.
...

Copyright 2022 furtidev

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


# Imports.
import aiohttp

from rich.align import Align
from rich.console import Console

from larryc.enums import ErrorType


# The App class for base operations.
class App:
	def __init__(self):
		self.console = Console()
		self.color = "green"

	async def run(self, word: str):
		session = aiohttp.ClientSession()

		async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as request:
			response = await request.json()

		await session.close()
		synonyms = []
		
		try:
			synonyms = response[0]['meanings'][0]['synonyms']
		except KeyError:
			pass

		if "message" in response:
			self.console.print(f"[red]ERROR:[/red] [green]{response['message']}[/green]")

		else:
			self.console.rule(f"🔍 Viewing Word -> [green]{word.capitalize()}[/green]")
			self.console.print(Align(":book: Definitions", align="center"))

			for i in range(len(response[0]['meanings'][0]['definitions'])):
				if self.color == "green":
					self.color = "yellow"
 
				else:
					self.color = "green"
					
				self.console.print(f"[{self.color}]• {response[0]['meanings'][0]['definitions'][i]['definition']}[/]", justify="center")
			
			if synonyms:
				self.console.rule("Synoyms")
				for i in synonyms:
					self.console.print(f"[cyan]{i}[/]", justify="center")
			
			
			self.console.rule(f"Made with [b magenta not dim]Rich[/]", characters="~", style="magenta")
			

	def err(self, type: ErrorType):
		if type == ErrorType.NO_ARG:
			self.console.print("[red]USAGE:[/red] [bold green]$ larryc <word>[/bold green]")
