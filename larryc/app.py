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
from functools import cache
from typing import Any, List

from rich.align import Align
from rich.console import Console

from larryc.enums import ErrorType


# The App class for base operations.
class App:
	def __init__(self) -> None:
		self.response = None
		self.console = Console()
		self.color = "green"

	async def call(self, word: str) -> None:
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as request:
				self.response = await request.json()
				return self.response
				
	def filter_definitions(self, sanitize: bool=True) -> List[str] | Any:
		try:
			definitions = self.response[0]['meanings'][0]['definitions']
		except KeyError:
			return None

		if not sanitize:
			return definitions

		sanitized = []
		for i in range(len(definitions)):
			sanitized.append(definitions[i]['definition'])

		return sanitized

	def filter_meanings(self, key: str) -> Any | None:
		try:
			return self.response[0]['meanings'][0][key]
		except KeyError:
			return None

	async def run(self, word: str) -> None:
		await self.call(word)

		definitions = self.filter_definitions()
		synonyms = self.filter_meanings('synonyms')
		antonyms = self.filter_meanings('antonyms')

		if "message" in self.response:
			self.console.print(f"[red]ERROR:[/red] [green]{self.response['message']}[/green]")

		else:
			self.console.rule(f"🔍 Viewing Word -> [green]{word.capitalize()}[/green]")
			self.console.print(Align(":book: Definitions", align="center"))

			for item in definitions:
				if self.color == "green":
					self.color = "yellow"
				else:
					self.color = "green"
					
				self.console.print(f"[{self.color}]• {item}[/]", justify="center")
			
			if synonyms:
				self.console.rule("Synonyms")
				for item in synonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")

			if antonyms:
				self.console.rule("Antonyms")
				for item in antonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")
			
			self.console.rule(f"Made with [b magenta not dim]Rich[/]", characters="~", style="magenta")
			

	def err(self, type: ErrorType) -> None:
		if type == ErrorType.NO_ARG:
			self.console.print("[red]USAGE:[/red] [bold green]$ larryc <word>[/bold green]")
