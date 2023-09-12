# emojis
class Common:
    pass

class Emojis(Common):
    def __init__(self):
        pass
    ideas = {
        "📥🔗📜" : "A new way to express The input that you process With emojis that impress And convey more with less",
        "🖼️📷" : "A challenge to achieve The image that you perceive With cameras that retrieve And frames that interweave",
        "👏👏👏"  : "A praise for your creation The emoji translation With innovation and imagination And a poetic celebration" ,
        "📥" :{ "type": "input"},
        
        "🔗" : { "url": "<URL>" },
        "📜" : { "value" : "<VALUE>" }

    }
    reversed = {
        "A": "🅰️",
        "new": "🆕"
    }
    # emit new source code with new constants
    # save in session save buffer
    def prompt_model(self, text):
        for x in ["Create prompt model that will ",
                  "Construct a prompt that will have the effect of ",
                  "Imagine instructions will have the effect of ",
                  "Instructions for",
                  "Instructions about",
                  "Structure of",
                  "Construction of",
                  "Deconstruction of",
                  "Reconstruction of",
                  "Critical Reconstruction of"]:
            yield { "combine" : [ x,text] }
            
    def lookup_ai(self,term, **args):
        yield from self.prompt_model(f"define the {term} with args {args} using example :'''{{data.text.raw}}'''")
    
    def lookup_emoji(self,x):
        if not isinstance(x,str):
            return
        if x in self.ideas:
            return #have it
        
        if x not in self.reversed:
            yield from self.lookup_ai("We need an Emoji")
            yield from self.lookup_ai(f"Consider the meaning of the term '{x}'")        
            yield from self.lookup_ai(f"Generate a Prompt to help find out the answer to the question of what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"help find out the answer to the question of what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"What are some Emojis for {x}?")        
            self.reversed[x] = "TODO"
    
    def process(self):
        # \'{data.text.raw}\'
        prmt= self.prompt_model(f"Answer the following question: What is the meaning of following Emoji: '''{{data.text.raw}}'''")
        
        for e in self.ideas:
            #st.write(e)
            yield from  self.lookup_ai(prmt,**{"emoji":e})            
            v = self.ideas[e]
            if isinstance(v,str):
                for x in v.split():
                    #st.write(e, x)
                    self.lookup_emoji(e)
                    self.lookup_emoji(x)
            elif isinstance(v,dict): #could be a word
                for k in v: #key name
                    v2 = v[k] #can be dic
                    if isinstance(v2, dict):
                        for k2 in v2:
                            v3 = v2[k2] # thied level
                            for a in [e, v, k, v2, k2, v3]:
                                self.lookup_emoji(a)

                            #st.write(e, v, k, v2, k2, v3)
                    else:
                        #st.write(e, v, k, v2)
                        pass
            #for a in [e, v, k, v2]:
            #    lookup_emoji(a)
        else:        
            for x in self.ideas[e]:
                #st.write(e, x)
                for a in [e, x]:
                    self.lookup_emoji(a)

    def toemoji(self,data):
        self.toprompt("translate this into a structured emoji representation?",data)

    def load_data(self):
        dataset = []
        text_data = resources_pb2.Text(raw=fstr)
        data = resources_pb2.Data(text=text_data)
        input_proto = resources_pb2.Input(
            data=data,
        )
        dataset.append(input_proto)
        return dataset
    
def main():
    m  = Emojis()
    for x in m.process():
        print(x)
#models = {

#    "App": Apps(),
#    "DataSet": DataSets(),
#    "PythonGlobals": Globals(),
#    "PythonTypes": Types(),
#    "PythonAsts": Asts(),
#}
if __name__ == "__main__" :
    main()
