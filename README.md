# Junk, Not-Junk Detector

This tool is built to do just one simple task: detect junk and not-junk texts from a variety of languages.
Just like that famous [hotdog not-hotdog](https://www.youtube.com/watch?v=pqTntG1RXSY), but applied on natural language text.
It can be very useful to test tools that extract, decompress, and/or decrypt natural language texts.


# Setup
Uses [fairseq](https://github.com/pytorch/fairseq)

```bash
# Optionally create a brand new conda environment for this
#conda create -n junkdetect python=3.7 pip 
#conda activate junkdetect

# Installing directly from github
pip install git+https://github.com/thammegowda/junkdetect

# Installing after cloning this repo
git clone https://github.com/thammegowda/junkdetect
cd junkdetect
pip install .

```
## How to use
Once you install it via pip, `junkdetect` or `python -m junkdetect` can be used to invoke from commandline
```bash
printf "This is a good sentence. \nT6785*&^T is 747658 you T&*^\n" | junkdetect
0.999824	This is a good sentence.
0.0747487	T6785*&^T is 747658 you T&*^
```
The output is one line per input, with two column separated  by `\t`. 
The first column has `perplexity`: a higher value implies not good not-junk, and lower means junk.
If you dont want input sentences back, use `cat input.txt | junkdetect | cut -f1 > scores.txt`

# How does this work
*junkdetect* looks like only a few lines of python code, but under the hood, it hides a great deal of complexity.  
It uses perplexity from neural (masked/auto-regressive) language models that are trained on tera bytes of web text
to tell junk and not-junk apart.   
Specifically, it uses Facebookresearch's [XML-R](https://github.com/facebookresearch/XLM/) retrieved from [torch.hub](https://pytorch.org/hub/).
Quoting the original developers of XML-R and [their paper, (see Table 6)](https://arxiv.org/pdf/1911.02116.pdf)
> XLM-R handles the following 100 languages: Afrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Basque, Belarusian, Bengali, Bengali Romanized, Bosnian, Breton, Bulgarian, Burmese, Burmese, Catalan, Chinese (Simplified), Chinese (Traditional), Croatian, Czech, Danish, Dutch, English, Esperanto, Estonian, Filipino, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Hausa, Hebrew, Hindi, Hindi Romanized, Hungarian, Icelandic, Indonesian, Irish, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Kurdish (Kurmanji), Kyrgyz, Lao, Latin, Latvian, Lithuanian, Macedonian, Malagasy, Malay, Malayalam, Marathi, Mongolian, Nepali, Norwegian, Oriya, Oromo, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskri, Scottish, Gaelic, Serbian, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tamil, Tamil Romanized, Telugu, Telugu Romanized, Thai, Turkish, Ukrainian, Urdu, Urdu Romanized, Uyghur, Uzbek, Vietnamese, Welsh, Western, Frisian, Xhosa, Yiddish.


## Back Story and Acknowledgements:
- This idea came out of discussion with [Tim Allison](https://twitter.com/_tallison).
He said it was hard to tell whether text was correctly extracted or not from files like PDFs using Apache Tika.
Thanks to him for making me think of something like this.
- I had read Facebook's very nice [XML-R paper of Conneau et al](https://arxiv.org/abs/1911.02116) and it was top of my mind. 
Although XLM folks [didnt help me get perplexity, and I had to dug it out of their code by myself](https://github.com/facebookresearch/XLM/issues/272), 
 I still like to thank them for making such useful pretrained models available for easy to use via `torch.hub`.

## Developers:
- [Thamme Gowda](https://twitter.com/thammegowda)  (wrote the version 0.1)
