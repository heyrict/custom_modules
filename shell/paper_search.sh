## paper search engine
alias webofscience="browse http://apps.webofknowledge.com/"
alias sciencedirect="browse http://www.sciencedirect.com/"

pubmed(){
    if test $# -eq 0
    then
        browse https://www.ncbi.nlm.nih.gov/pubmed
    else
        local str=""
        for i in $*;do str=$str"+"$i;done
        browse https://www.ncbi.nlm.nih.gov/pubmed?term=${str:1}
    fi
}

pmid(){
    browse https://www.ncbi.nlm.nih.gov/pubmed/$1
}

ncbi(){
    if test $# -eq 0
    then
        browse https://www.ncbi.nlm.nih.gov/
    else
        local str=""
        for i in $*;do str=$str"+"$i;done
        browse https://www.ncbi.nlm.nih.gov/gquery/?term=${str:1}
    fi
}

nature(){
    if test $# -eq 0
    then
        browse https://www.nature.com/
    else
        local str=""
        for i in $*;do str=$str"+"$i;done
        browse https://www.nature.com/search?q=${str:1}
    fi
}

wanfang(){
    if test $# -eq 0
    then
        browse http://s.g.wanfangdata.com.cn
    else
        local str=""
        for i in $*;do str=$str"+"$i;done
        browse http://s.g.wanfangdata.com.cn/Paper.aspx?q=${str:1}
    fi
}
