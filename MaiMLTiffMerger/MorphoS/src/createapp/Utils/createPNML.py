################################################
##   Util class
################################################
import copy
import xmltodict

from django.conf import settings
from .staticClass import maimlelement

################################################
##   Util class
################################################
class MaimlUtilforPNML():

    @classmethod
    def gettemplateidlist(self, parentList):
        midlist = []
        cidlist = []
        ridlist = []
        if isinstance(parentList,list):
            pass
        else:
            parentList = [parentList]
        for parentdict in parentList:
            if maimlelement.materialTemplate in parentdict.keys():
                # place --allM
                mtlist = parentdict[maimlelement.materialTemplate]
                if isinstance(mtlist,list):
                    pass
                else:
                    mtlist = [mtlist]
                for mtdict in mtlist:
                    mtdictref = mtdict[maimlelement.placeRef]
                    if isinstance(mtdictref,list):
                        pass
                    else:
                        mtdictref = [mtdictref]
                    for mplace in mtdictref:
                        midlist.append(str(mplace[maimlelement.refd]))
            if maimlelement.conditionTemplate in parentdict.keys():
                ctlist = parentdict[maimlelement.conditionTemplate]
                if isinstance(ctlist,list):
                    pass
                else:
                    ctlist = [ctlist]
                for ctdict in ctlist:
                    ctdictref = ctdict[maimlelement.placeRef]
                    if isinstance(ctdictref,list):
                        pass
                    else:
                        ctdictref = [ctdictref]
                    for cplace in ctdictref:
                        cidlist.append(str(cplace[maimlelement.refd]))
            if maimlelement.resultTemplate in parentdict.keys():
                rtlist = parentdict[maimlelement.resultTemplate]
                if isinstance(rtlist,list):
                    pass
                else:
                    rtlist = [rtlist]
                for rtdict in rtlist:
                    rtdictref = rtdict[maimlelement.placeRef]
                    if isinstance(rtdictref,list):
                        pass
                    else:
                        rtdictref = [rtdictref]
                    for rplace in rtdictref:
                        ridlist.append(str(rplace[maimlelement.refd]))

        return midlist, cidlist, ridlist

    def makepnmlgraphdata(cls, maimldict):
        petrinetdata = []
        pnml_dict = maimldict[maimlelement.maiml][maimlelement.protocol][maimlelement.method][maimlelement.pnml]
        transition_list = []
        if isinstance(pnml_dict[maimlelement.transition], list):
            transition_list = copy.deepcopy(pnml_dict[maimlelement.transition])
        else:
            transition_list = copy.deepcopy([pnml_dict[maimlelement.transition]])

        midlist = []
        cidlist = []
        ridlist = []

        program_list = maimldict[maimlelement.maiml][maimlelement.protocol][maimlelement.method][maimlelement.program]
        if isinstance(program_list,list):
            pass
        else:
            program_list = [program_list]
        pr_midlist, pr_cidlist, pr_ridlist = cls.gettemplateidlist(program_list)
        midlist += pr_midlist
        cidlist += pr_cidlist
        ridlist += pr_ridlist

        method_list = maimldict[maimlelement.maiml][maimlelement.protocol][maimlelement.method]
        if isinstance(method_list,list):
            pass
        else:
            method_list = [method_list]
        mt_midlist, mt_cidlist, mt_ridlist = cls.gettemplateidlist(method_list)
        midlist += mt_midlist
        cidlist += mt_cidlist
        ridlist += mt_ridlist

        protocol_list = maimldict[maimlelement.maiml][maimlelement.protocol]
        if isinstance(protocol_list,list):
            pass
        else:
            protocol_list = [protocol_list]
        pt_midlist, pt_cidlist, pt_ridlist = cls.gettemplateidlist(protocol_list)
        midlist += pt_midlist
        cidlist += pt_cidlist
        ridlist += pt_ridlist

        if isinstance(pnml_dict[maimlelement.place], list):
            place_list = copy.deepcopy(pnml_dict[maimlelement.place])
        else:
            place_list = copy.deepcopy([pnml_dict[maimlelement.place]])
        for place_dict in place_list:
            maiml_type='M'
            if str(place_dict[maimlelement.idd]) in cidlist:
                maiml_type = "C"
            if str(place_dict[maimlelement.idd]) in ridlist:
                maiml_type = "R"

            petrinetdata.append({"data": {"id": str(place_dict[maimlelement.idd]), "maiml_type":maiml_type}})
        # transition
        if isinstance(transition_list, list):
            pass
        else:
            transition_list = [transition_list]
        for transition_dict in transition_list:
            petrinetdata.append({"data": {"id": str(transition_dict[maimlelement.idd]), "maiml_type":"T"}})
        # arc
        if isinstance(pnml_dict[maimlelement.arc], list):
            arc_list = copy.deepcopy(pnml_dict[maimlelement.arc])
        else:
            arc_list = copy.deepcopy([pnml_dict[maimlelement.arc]])
        for arc_dict in arc_list:
            petrinetdata.append({"data": {"id": str(arc_dict[maimlelement.idd]), "source": str(arc_dict[maimlelement.sourced]), "target": str(arc_dict[maimlelement.targetd]), "nodeType":"transition",}})

        petrinetdata2 = [
                # node(place,transition)
                {"data": {"id": "M1id", "maiml_type": "M"},},
                {"data": {"id": "C1id", "maiml_type": "C"},},
                {"data": {"id": "T1id", "maiml_type": "T"},},
                {"data": {"id": "R1id", "maiml_type": "R"},},
                # edge(arc)
                {"data": {"id": "arc1id", "source": "M1id", "target": "T1id", "nodeType":"transition", "label": "M1 - T1"},},
                {"data": {"id": "arc2id", "source": "C1id", "target": "T1id", "nodeType":"transition", "label": "C1 - T1"},},
                {"data": {"id": "arc3id", "source": "T1id", "target": "R1id", "nodeType":"transition", "label": "C - D"},},
        ]
        return petrinetdata
    