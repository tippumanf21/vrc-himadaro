# pipenvインストール
pip install pipenv

# 現在のディレクトリにvenv環境を作成する
$env:PIPENV_VENV_IN_PROJECT=1

# pipfileから環境生成
pipenv install --dev
