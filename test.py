import re

regex = r"(Chromium|Chrome)/(\d+)\.(\d+)(?:\.(\d+))?"
regex = r"^(?!.*Edge).*Chrome"

string = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

print(re.match(regex, string))