#!bash

#typescript
./node_modules/.bin/tsc --init

index_typescript="\

import  '../styles/styles.scss';

window.onload = ()=> {
  console.log(window.location.href);
}

"
echo "$index_typescript" > ./src/typescript/index.ts

cat <<EOF
####################################################
ATTENZIONE 
####################################################

controllare le impostazioni basilari nel file di configurazione TSCONFIG.json

        {
            "compilerOptions": {
                "module": "es2015",
                "target": "es6",
                "outDir": ".\/dist",
                "strict": false,
                "lib": [
                    "DOM",
                    "ES2016"
                ],
                "skipLibCheck": true,
                "forceConsistentCasingInFileNames": true,
                "esModuleInterop": true,
                "moduleResolution": "node"
            },
            "exclude": [
                "node_modules",
                "**\/*.spec.ts"
            ]
        }
EOF