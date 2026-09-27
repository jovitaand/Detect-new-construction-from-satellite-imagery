"""RGB absolute-difference baseline. Scores are NOT probabilities."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image

def evaluate(pred, truth):
    tp=int(np.sum(pred & truth)); fp=int(np.sum(pred & ~truth))
    fn=int(np.sum(~pred & truth)); tn=int(np.sum(~pred & ~truth))
    def ratio(n,d): return n/d if d else None
    return dict(tp=tp,fp=fp,fn=fn,tn=tn,precision=ratio(tp,tp+fp),
                recall=ratio(tp,tp+fn),f1=ratio(2*tp,2*tp+fp+fn),iou=ratio(tp,tp+fp+fn))

def run(before, after, out, threshold=0.2, label=None):
    if not 0 <= threshold <= 1: raise ValueError('threshold must be in [0, 1]')
    a=np.asarray(Image.open(before).convert('RGB'),dtype=np.float32)/255
    b=np.asarray(Image.open(after).convert('RGB'),dtype=np.float32)/255
    if a.shape != b.shape: raise ValueError('Images must have the same shape and be aligned')
    score=np.abs(b-a).mean(axis=2)
    pred=score > threshold
    result={'method':'mean_absolute_RGB_difference','threshold':threshold,
            'changed_pixel_fraction':float(pred.mean()),'score_is_probability':False}
    if label:
        truth_array=np.asarray(Image.open(label).convert('L'))
        if truth_array.shape != pred.shape: raise ValueError('Label shape differs')
        if not set(np.unique(truth_array)).issubset({0,1,255}):
            raise ValueError('Expected binary labels encoded 0/1 or 0/255')
        result['metrics']=evaluate(pred,truth_array>0)
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    Image.fromarray((pred.astype(np.uint8)*255)).save(out/'prediction.png')
    Image.fromarray((score*255).astype(np.uint8)).save(out/'difference.png')
    overlay=(b*255).astype(np.uint8)
    overlay[pred]=(0.45*overlay[pred]+0.55*np.array([255,0,0])).astype(np.uint8)
    panels=np.concatenate([(a*255).astype(np.uint8),(b*255).astype(np.uint8),overlay],axis=1)
    Image.fromarray(panels).save(out/'before_after_overlay.png')
    (out/'metrics.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before',required=True); parser.add_argument('--after',required=True)
    parser.add_argument('--label'); parser.add_argument('--out',default='outputs/baseline')
    parser.add_argument('--threshold',type=float,default=0.2)
    args=parser.parse_args()
    print(json.dumps(run(args.before,args.after,args.out,args.threshold,args.label),indent=2))
