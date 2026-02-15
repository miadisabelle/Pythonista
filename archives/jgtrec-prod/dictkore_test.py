
import coaiamodule as co

otezt="""
These are textual content, too. Go with the artwork. Can you create mostly motivated by complacency? That is a great question, isn't it? The truth is you truly create for love. 
"""

"""
This text is also a form of content, isn't it? It complements the artwork. Can one create primarily out of complacency? That's an intriguing question, isn't it? The reality is that creation is driven by passion.

"""

try:
	r=co.dictkore_send(otezt)
	print(r)
except Exception as ex:
	print(ex)

