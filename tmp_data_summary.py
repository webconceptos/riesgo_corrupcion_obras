import pandas as pd
from pathlib import Path
import json

base = Path('c:/IA_Investigacion/Deteccion_Corrupcion')
processed = base / 'data' / 'processed'
print('Processed files:')
for p in sorted(processed.glob('*.parquet')):
    df = pd.read_parquet(p)
    print(f'\n{p.name}: shape={df.shape}')
    print(' columns=', len(df.columns), 'target cols sample=', [c for c in df.columns if 'target' in c.lower() or 'riesgo' in c.lower()][:5])
    print(' dtypes=', df.dtypes.value_counts().to_dict())
    miss = df.isna().sum()
    miss = miss[miss > 0].sort_values(ascending=False)
    print(' missing cols=', len(miss))
    print(' top missing=', miss.head(10).to_dict())
    if 'target' in df.columns or 'y_riesgo' in df.columns or 'riesgo' in df.columns:
        tgt = [c for c in df.columns if c.lower() in ('target', 'y_riesgo', 'riesgo')][0]
        print(' target values:', df[tgt].value_counts(dropna=False).to_dict())
    if p.name == 'dataset_integrado.parquet':
        print(' top 10 cols by unique count:', df.nunique().sort_values(ascending=False).head(10).to_dict())
        print(' sample cols:', df.columns.tolist()[:20])
