# The Corpus object

`Corpus` can model collections of unparsed or parsed data. It's probably the only class you will ever need to import from `buzz`.

All you need to get started is a directory containing plain text files, optionally within subdirectories, which will be understood as subcorpora.

## Corpus methods


```python
from buzz import Corpus
corpus = Corpus('dtrt/do-the-right-thing')
print(corpus.files[0].path)
# `dtrt/do-the-right-thing/01-we-love-radio-station-storefront.txt`
corpus.files[0].read()
```

```
WE SEE only big white teeth and very Negroidal (big) lips. <metadata time="DAY" loc="INT" setting="WE LOVE RADIO STATION STOREFRONT" scene="1" stage_direction="true">
Waaaake up! Wake up! Wake up! Wake up! Up ya wake! Up ya wake! Up ya wake!. <metadata time="DAY" loc="INT" setting="WE LOVE RADIO STATION STOREFRONT" scene="1" stage_direction="true" speaker="MISTER SEÑOR LOVE DADDY" line="1"> <metadata time="DAY" loc="INT" setting="WE LOVE RADIO STATION STOREFRONT" scene="1" stage_direction="true" speaker="MISTER SEÑOR LOVE DADDY" line="1">
This is Mister Señor Love Daddy. Your voice of choice. The world's only twelve-hour strongman, here on WE LOVE radio, 108 FM. The last on your dial, but the first in ya hearts, and that's the truth, Ruth!. <metadata time="DAY" loc="INT" setting="WE LOVE RADIO STATION STOREFRONT" scene="1" stage_direction="true" speaker="MISTER SEÑOR LOVE DADDY" line="2"> <metadata time="DAY" loc="INT" setting="WE LOVE RADIO STATION STOREFRONT" scene="1" stage_direction="true" speaker="MISTER SEÑOR LOVE DADDY" line="2">
```

## Parsing a corpus

The `parse` method of Corpus objects will do a full dependency and constituency parse of the text, including lemmatisation, POS tagging, and so on. The result will be stored in a new directory with the same structure as the unparsed corpus, with each file now being formatted as CONLL-U 2.0.

```python
parsed = corpus.parse()
print(parsed)
# <buzz.corpus.Corpus object at 0x7fb2f3af6470 (dtrt/do-the-right-thing-parsed, parsed)>
print(parsed.files[0].path)
# `dtrt/do-the-right-thing-parsed/01-we-love-radio-station-storefront.txt.conllu`
print(parsed.files[0].read())
```

```
# loc = INT
# parse = (S (NP (PRP WE)) (VP (VBP SEE) (NP (NP (RB only) (JJ big) (JJ white) (NNS teeth)) (CC and) (NP (ADJP (ADJP (RB very) (JJ Negroidal)) (PRN (-LRB- -LRB-) (JJ big) (-RRB- -RRB-))) (NNS lips)))) (. .) (  ))
# scene = 1
# sent_id = 1
# sent_len = 15
# setting = WE LOVE RADIO STATION STOREFRONT
# stage_direction = True
# text = WE SEE only big white teeth and very Negroidal (big) lips.
# time = DAY
1	WE	we	PRON	PRP	_	2	nsubj	_	_
2	SEE	see	VERB	VBP	_	0	ROOT	_	_
3	only	only	ADV	RB	_	6	advmod	_	_
4	big	big	ADJ	JJ	_	6	amod	_	_
5	white	white	ADJ	JJ	_	6	amod	_	_
6	teeth	tooth	NOUN	NNS	_	2	dobj	_	_
7	and	and	CCONJ	CC	_	6	cc	_	_
8	very	very	ADV	RB	_	9	amod	_	_
9	Negroidal	negroidal	ADJ	JJ	_	6	conj	_	_
10	(	(	PUNCT	-LRB-	_	9	punct	_	_
11	big	big	ADJ	JJ	_	13	amod	_	_
12	)	)	PUNCT	-RRB-	_	13	punct	_	_
13	lips	lip	NOUN	NNS	_	9	appos	_	_
14	.	.	PUNCT	.	_	2	punct	_	_
```

## Load corpus into memory

```python
loaded = parsed.load()
print(loaded)
print(loaded.iloc[0:8, 0:6].to_html())
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th>w</th>
      <th>l</th>
      <th>x</th>
      <th>p</th>
      <th>g</th>
      <th>f</th>
    </tr>
    <tr>
      <th align="right">file</th>
      <th>s</th>
      <th>i</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="8" valign="top">01-we-love-radio-station-storefront</th>
      <th rowspan="8" valign="top">1</th>
      <th>1</th>
      <td>WE</td>
      <td>we</td>
      <td>PRON</td>
      <td>PRP</td>
      <td>2</td>
      <td>nsubj</td>
    </tr>
    <tr>
      <th align="right">2</th>
      <td>SEE</td>
      <td>see</td>
      <td>VERB</td>
      <td>VBP</td>
      <td>0</td>
      <td>ROOT</td>
    </tr>
    <tr>
      <th align="right">3</th>
      <td>only</td>
      <td>only</td>
      <td>ADV</td>
      <td>RB</td>
      <td>6</td>
      <td>advmod</td>
    </tr>
    <tr>
      <th align="right">4</th>
      <td>big</td>
      <td>big</td>
      <td>ADJ</td>
      <td>JJ</td>
      <td>6</td>
      <td>amod</td>
    </tr>
    <tr>
      <th align="right">5</th>
      <td>white</td>
      <td>white</td>
      <td>ADJ</td>
      <td>JJ</td>
      <td>6</td>
      <td>amod</td>
    </tr>
    <tr>
      <th align="right">6</th>
      <td>teeth</td>
      <td>tooth</td>
      <td>NOUN</td>
      <td>NNS</td>
      <td>2</td>
      <td>dobj</td>
    </tr>
    <tr>
      <th align="right">7</th>
      <td>and</td>
      <td>and</td>
      <td>CCONJ</td>
      <td>CC</td>
      <td>6</td>
      <td>cc</td>
    </tr>
    <tr>
      <th align="right">8</th>
      <td>very</td>
      <td>very</td>
      <td>ADV</td>
      <td>RB</td>
      <td>9</td>
      <td>amod</td>
    </tr>
  </tbody>
</table>

All metadata attributes are available for each token in the text.


```python
print(loaded.head(1).T.to_html())
```

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th align="right">file</th>
      <th>01-we-love-radio-station-storefront</th>
    </tr>
    <tr>
      <th align="right">s</th>
      <th>1</th>
    </tr>
    <tr>
      <th align="right">i</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th align="right">w</th>
      <td>WE</td>
    </tr>
    <tr>
      <th align="right">l</th>
      <td>we</td>
    </tr>
    <tr>
      <th align="right">x</th>
      <td>PRON</td>
    </tr>
    <tr>
      <th align="right">p</th>
      <td>PRP</td>
    </tr>
    <tr>
      <th align="right">g</th>
      <td>2</td>
    </tr>
    <tr>
      <th align="right">f</th>
      <td>nsubj</td>
    </tr>
    <tr>
      <th align="right">e</th>
      <td>_</td>
    </tr>
    <tr>
      <th align="right">loc</th>
      <td>INT</td>
    </tr>
    <tr>
      <th align="right">parse</th>
      <td>(S (NP (PRP WE)) (VP (VBP SEE) (NP (NP (RB onl...</td>
    </tr>
    <tr>
      <th align="right">scene</th>
      <td>1</td>
    </tr>
    <tr>
      <th align="right">sent_id</th>
      <td>1</td>
    </tr>
    <tr>
      <th align="right">sent_len</th>
      <td>15</td>
    </tr>
    <tr>
      <th align="right">setting</th>
      <td>WE LOVE RADIO STATION STOREFRONT</td>
    </tr>
    <tr>
      <th align="right">stage_direction</th>
      <td>True</td>
    </tr>
    <tr>
      <th align="right">text</th>
      <td>WE SEE only big white teeth and very Negroidal...</td>
    </tr>
    <tr>
      <th align="right">time</th>
      <td>DAY</td>
    </tr>
  </tbody>
</table>