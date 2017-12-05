from nltk.corpus import wordnet


def word_lemmas(word_input):
	word_relations_list = wordnet.synsets(word_input)

	final_lemma_list = []

	for elem in word_relations_list:
		for lemma in elem.lemmas():
			lemma_name = lemma.name()
			if lemma_name not in final_lemma_list:
				final_lemma_list.append(lemma_name)

	return final_lemma_list
	# for i in final_lemma_list:
	# 	print(i)
