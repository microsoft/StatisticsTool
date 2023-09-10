 def get_TP_FP_FN_masks(comp_data, **kwargs):
        """
        :param comp_data: 
        :return: Boolean masks of TP, FP, FN that indicates which row in the predictions dataframe is TP/FP
                 and which row in the labels dataframe is a FN (row = bounding box)
        """
        #first key from 'detection' key in input
        key = 'detection'
        FN_mask = (comp_data[key+'_gt']==True) & (comp_data[key]==False)
        FP_mask = (comp_data[key]==True) & (comp_data[key+'_gt']==False)
        TP_mask = (comp_data[key]==True) & (comp_data[key+'_gt']==True)
        TN_mask = (comp_data[key+'_gt']==False) & (comp_data[key]==False)
        
        return {"TP":TP_mask, "FP":FP_mask, "FN":FN_mask, "TN":TN_mask}
               