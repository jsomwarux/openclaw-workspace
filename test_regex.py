import re

tests = [
	'[Hook — "28% APY sounds like free money. Here\'s what game theory actually sees."]',
	'[The staking APY on screen — labeled as "a common take: 28% APY"]',
	'[Why high APY is structurally a prisoner\'s dilemma — 1-2 sentences]',
	'The yield is the trap, not the signal.'
]

for t in tests:
	extracted = t
	# 1. if it starts with [ and ends with ] and contains a quote, extract the quote
	m_quote = re.search(r'\[.*?["”](.*?)["”].*?\]', t)
	if m_quote:
		extracted = m_quote.group(1)
	else:
		# 2. if it starts with [ and ends with ], just remove the brackets and 'Hook — ' type prefixes
		m_bracket = re.match(r'^\[(.*?)\]$', t)
		if m_bracket:
			inner = m_bracket.group(1)
			inner = re.sub(r'^(?:Hook|The insight|CTA).*?—\s*', '', inner, flags=re.IGNORECASE)
			extracted = inner
	print(f"Original: {t}\nCleaned: {extracted}\n")
