import spacy
import csv
from spacy.symbols import acomp,advcl,advmod,agent,amod,appos,attr,aux,auxpass,cc,ccomp,complm,conj,csubj,csubjpass,dep,det,dobj,expl,infmod,intj,iobj,mark,meta,neg,nmod,nn,npadvmod,nsubj,nsubjpass,num,number,oprd,parataxis,partmod,pcomp,pobj,poss,possessive,preconj,prep,prt,punct,quantmod,rcmod,root,xcomp,hmod
import pickle
# import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
# nlp=en_core_web_sm.load()
deps_vc_list =[aux,auxpass,prt]
deps_list = [pobj,advmod,dobj,iobj]
verb_tags = ["MD","VB","VBD","VBG","VBN","VBP","VBZ","RP","TO"]
perf_tenses=["past_perfect","past_perfect_cont","pres_perfect","pres_perfect_cont","fut_perfect","fut_perfect_cont","PApast_perfect","PApres_perfect","PAfut_perfect"]

# creates a verb chain from the sentence : verb chain is the list of POS tags of children of the verb, Rules determining the tense of a verb chain in pickle_src
# based on verb chain returns fine tense, voice, True/False (if the tense is a perfect tense) and modal (if present) of the given verb
def get_eve_tense_voice(ev_node): # pass as argument the verb node from spacy sentence
    v_cha ={}
    v_list=[]
    temp_pic=open('tense.p','rb')
    pickle_src = pickle.load(temp_pic) # loads the  rules to be followed to extract tense
    v_cha[ev_node.i]=ev_node.tag_
    v_list.append(ev_node.lemma_)
    for w in ev_node.children:
        if w.tag_ in verb_tags:
            v_cha[w.i]=w.tag_
            v_list.append(w.lemma_)
    v_ch = ""
    for k in sorted(v_cha.keys()):
        v_ch = v_ch+ str(v_cha[k])+" "
        v_ch=v_ch.strip()
    voice="None"
    ev_tense = "None"
    modals = []
    for v in v_list:
        if v.lower() in pickle_src:
            modals.append(pickle_src[v.lower()])
    if len(modals) > 0:
        modal = modals[0]
    else:
        modal = "None"
    if v_ch in pickle_src:
        t = pickle_src[v_ch]
        if t == "PAinfinitives":
            voice = "passive"
            ev_tense = "infinitives"
        elif t == "infinitives":
            voice = "active"
            ev_tense = "infinitives"
        elif t== "past_perfect_cont":
            voice = "active"
            ev_tense = "past_perfect_cont"
        elif t == "PApast_perfect":
            voice = "passive"
            ev_tense = "past_perfect"
        elif t == "past_perf" and ("was" in v_list or "were" in v_list):
            voice = "active"
            ev_tense = "past_perf"
        elif t == "PApast_cont":
            voice = "passive"
            ev_tense = "past_cont"
        elif t == "past_cont":
            voice = "active"
            ev_tense = "past_cont"
        elif t == "PAsim_past" and ("was" in v_list or "were" in v_list):
            voice = "passive"
            ev_tense = "sim_past"
        elif t == "sim_past":
            voice = "active"
            ev_tense = "sim_past"
        elif t == "pres_perfect_cont":
            voice = "active"
            ev_tense = "pres_perfect_cont"
        elif t == "PApres_perfect":
            ev_tense = "pres_perfect"
            voice = "passive"
        elif t == "pres_perfect" and ("is" in v_list or "are" in v_list):
            voice = "active"
            ev_tense = "pres_perfect"
        elif t == "PApres_cont":
            voice = "passive"
            ev_tense = "pres_cont"
        elif t == "pres_cont":
            voice = "active"
            ev_tense = "pres_cont"
        elif t == "PApres" and ("is" in v_list or "are" in v_list):
            voice = "passive"
            ev_tense = "pres"
        elif t == "pres":
            voice = "active"
            ev_tense = "pres"
        elif t == "fut_perfect_cont"  and ("fut_modal" in modals):
            voice = "passive"
            ev_tense = "fut_perferct_cont"
        elif t == "PAfut_perfect" and ("fut_modal" in modals):
            voice = "passive"
            ev_tense = "fut_perfect"
        elif t == "PAfut" and "fut_modal" in modals:
            ev_tense = "fut"
            if "be" in v_list:
                voice = "passive"
            else:
                voice = "active"
        elif t == "PAfut_cont" and "fut_modal" in modals:
            ev_tense = "fut_cont"
            voice = "passive"
        elif t == "fut_cont" and "fut_modal" in modals:
            voice = "active"
            ev_tense = "fut_cont"
        elif t == "fut" and "fut_modal" in modals:
            voice = "active"
            ev_tense = "fut"
        elif t == "fut_perfect_cont"  and "cond_modal" in modals:
            voice = "active"
            ev_tense = "fut_perfect_cont"
        elif t == "PAfut_perfect" and "cond_modal" in modals:
            voice = "passive"
            ev_tense = "fut_perfect"
        elif t == "fut_perfect" and "cond_modal" in modals:
            ev_tense = "fut_perfect"
            if "be" in v_list:
                voice = "passive"
            else:
                voice = "active"
        elif t == "PAfut_cont" and "cond_modal" in modals:
            voice = "passive"
            ev_tense = "fut_cont"
        elif t == "fut_cont" and "cond_modal" in modals:
            voice = "active"
            ev_tense = "fut_cont"
        elif t == "fut" and "cond_modal" in modals:
            voice = "active"
            ev_tense = "fut"
        else:
            ev_tense = "other"
            voice = "unk"
    else:
        voice = "unk"

    is_perf = False
    if ev_tense in perf_tenses:
        is_perf = True
    return ev_tense,voice,is_perf,modal
# sent = nlp(u'John is playing.')

# since playing is the verb for which we need tense we pass it to the function that extracts tense

# print (get_eve_tense_voice(sent[2]))
# will print the fine tense, voice, True/False (if the tense is a perfect tense) and modal (if present)


# sent = nlp(u'John will play.')

# since playing is the verb for which we need tense we pass it to the function that extracts tense

# print (get_eve_tense_voice(sent[2]))
# will print the fine tense, voice, True/False (if the tense is a perfect tense) and modal (if present)

