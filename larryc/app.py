'''
The command-line parser for the package.
...

Copyright 2022 furtidev, HitBlast

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


# Imports.
import aiohttp
from typing import Any, List

from rich.align import Align
from rich.console import Console

from larryc.enums import ErrorType


# The Word class for keeping track of an API response.
class Word:
	def __init__(self, response: Any):
		self.response = response

	@property
	def phonetic(self) -> str | None:
		try:
			return self.response[0]['phonetic']
		except KeyError:
			return None

	@property
	def definitions(self) -> List[str] | None:
		try:
			definitions = self.response[0]['meanings'][0]['definitions']
		except KeyError:
			return None

		sanitized = []
		for i in range(len(definitions)):
			sanitized.append(definitions[i]['definition'])

		return sanitized

	@property
	def synonyms(self) -> Any | None:
		try:
			return self.response[0]['meanings'][0]['synonyms']
		except KeyError:
			return None

	@property
	def antonyms(self) -> Any | None:
		try:
			return self.response[0]['meanings'][0]['antonyms']
		except KeyError:
			return None



# The App class for base operations.
class App:
	def __init__(self) -> None:
		self.response = None
		self.console = Console()
		self.color = "green"

	async def call(self, word: str) -> Word:
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as request:
				self.response = await request.json()
				return Word(self.response)

	async def run(self, word: str) -> None:
		word_obj = await self.call(word)

		if "message" in self.response:
			self.console.print(f"[red]ERROR:[/red] [green]{self.response['message']}[/green]")

		else:
			self.console.rule(f"🔍 Viewing Word -> [green]{word.capitalize()} ({word_obj.phonetic if word_obj.phonetic else 'no phonetic'})[/green]")
			self.console.print(Align(":book: Definitions", align="center"))

			for item in word_obj.definitions:
				if self.color == "green":
					self.color = "yellow"
				else:
					self.color = "green"
					
				self.console.print(f"[{self.color}]• {item}[/]", justify="center")
			
			if word_obj.synonyms:
				self.console.rule("Synonyms")
				for item in word_obj.synonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")

			if word_obj.antonyms:
				self.console.rule("Antonyms")
				for item in word_obj.antonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")
			
			self.console.rule(f"Made with [b magenta not dim]Rich[/]", characters="~", style="magenta")
			

	def err(self, type: ErrorType) -> None:
		if type == ErrorType.NO_ARG:
			self.console.print("[red]USAGE:[/red] [bold green]$ larryc <word>[/bold green]")
