'''
The command-line parser for the package.
...

MIT License

Copyright (c) 2022 furtidev, HitBlast

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


# Imports.
import aiohttp
from typing import Any, List

from rich.style import Style
from rich.console import Console

from larryc.enums import ErrorType


# The Word class for keeping track of an API response.
class Word:
	def __init__(self, response: Any):
		self.response = response

	def __str__(self) -> str:
		return self.response[0]['word']

	@property
	def phonetics(self) -> List[str] | None:
		data = self.response[0]
		phonetic = []

		if 'phonetics' in data:
			data = self.response[0]['phonetics']

			for item in data:
				if 'text' in item:
					phonetic.append(item['text'])

		elif 'phonetic' in data:
			phonetic.append(data['phonetic'])

		return phonetic

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
		self.color = "yellow dim"

	async def call(self, word: str) -> Word:
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") as request:
				self.response = await request.json()
				return Word(self.response)

	async def run(self, word: str) -> None:
		word_obj = await self.call(word)

		if "message" in self.response:
			self.console.line()
			self.console.print(f"[red reverse] ERROR [/] {self.response['message']}", justify="center")
			self.console.line()

		else:
			self.console.line(2)
			self.console.print(f'[green]{word.capitalize()}[/]  |  Made with [bold purple]Rich[/]', justify="center")

			if word_obj.definitions:
				self.console.line()
				self.console.rule("[bold white]Definitions[/]")

				for item in word_obj.definitions:
					if self.color == "yellow":
						self.color += " dim"
					else:
						self.color = "yellow"
						
					self.console.print(f"[{self.color}]• {item}[/]", justify="center")

			if word_obj.phonetics:
				self.console.line()
				self.console.rule("[bold white]Phonetics[/]", style=None)

				for item in word_obj.phonetics:
					self.console.print(f"[cyan]{item}[/]", justify="center")
			
			if word_obj.synonyms:
				self.console.line()
				self.console.rule("[bold white]Synonyms[/]", style=None)

				for item in word_obj.synonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")

			if word_obj.antonyms:
				self.console.line()
				self.console.rule("[bold white]Antonyms[/]", style=None)

				for item in word_obj.antonyms:
					self.console.print(f"[cyan]{item}[/]", justify="center")
			
			self.console.line(2)
			

	def err(self, type: ErrorType) -> None:
		if type == ErrorType.NO_ARG:
			self.console.line()
			self.console.print("[red reverse] USAGE [/] $ larryc [green]<word>[/]", justify="center")
			self.console.line()
