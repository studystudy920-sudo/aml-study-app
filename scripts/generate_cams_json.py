#!/usr/bin/env python3
"""Generate CAMS exam questions JSON for the AML study app.

This script produces /home/user/aml-study-app/data/cams_questions.json
containing 80 CAMS questions across 4 domains.
"""

import json
import os

# ---------------------------------------------------------------------------
# Domain 1: ML/TF Risks and Methods  (Q1-Q35)
# ---------------------------------------------------------------------------
domain1_questions = [
    # ---- Deck 01 (Q1-Q5) ----
    {
        "id": "cams-d1-001",
        "question": "以下のシナリオのうち、人身売買・密輸（Human Smuggling/Trafficking）の疑わしい取引指標として最も該当するものはどれか。",
        "questionEn": "Which of the following scenarios is most indicative of a red flag for human smuggling or trafficking?",
        "options": [
            "A. 企業口座から定期的に行われる給与振込",
            "B. エスコートサービスへの頻繁な支払いと口座への高速度な現金入金の組み合わせ",
            "C. 小売業者による季節的な売上増減",
            "D. 個人口座から住宅ローンの毎月の返済"
        ],
        "answer": 1,
        "explanation": "エスコートサービスへの支払いと高速度の現金入金の組み合わせは、人身売買に関連する典型的な疑わしい取引指標です。人身売買では、性的搾取による収益が現金で頻繁に口座に入金され、エスコートサービスや類似業種への支払いが行われるパターンが見られます。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-002",
        "question": "PEP（Politically Exposed Person：重要な公的地位を有する者）の定義として最も正確なものはどれか。",
        "questionEn": "What is the most accurate definition of a Politically Exposed Person (PEP)?",
        "options": [
            "A. 重要な公的機能を委ねられた個人（国家元首、政府高官、軍幹部等）",
            "B. 政治献金を行うすべての個人",
            "C. 選挙に立候補したことのある個人",
            "D. 政府と契約関係にある企業の従業員"
        ],
        "answer": 0,
        "explanation": "PEPとは、国家元首、政府高官、軍の上級幹部、国有企業の経営幹部など、重要な公的機能を委ねられた（entrusted with prominent public function）個人を指します。FATFの定義に基づき、その家族や親しい関係者も含まれます。",
        "tags": ["pep", "cdd"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-003",
        "question": "マネー・ローンダリングのプレースメント（Placement）段階の定義として最も適切なものはどれか。",
        "questionEn": "Which of the following best defines the Placement stage of money laundering?",
        "options": [
            "A. 違法活動から得た現金を物理的に金融システムに投入すること",
            "B. 資金の出所を隠すために複数の取引を行うこと",
            "C. 洗浄された資金を合法的な経済活動に統合すること",
            "D. 犯罪収益を暗号資産に変換すること"
        ],
        "answer": 0,
        "explanation": "プレースメント（配置）とは、犯罪活動から得た現金を銀行口座への預け入れ、カジノでのチップ購入、高額商品の購入などを通じて金融システムに物理的に投入する最初の段階です。この段階が最も検知されやすいとされています。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": ["std-ch1-001"]
    },
    {
        "id": "cams-d1-004",
        "question": "前提犯罪（Predicate Offense）の定義として正しいものはどれか。",
        "questionEn": "What is a Predicate Offense in the context of money laundering?",
        "options": [
            "A. マネー・ローンダリング行為そのもの",
            "B. 規制当局への届出義務違反",
            "C. テロ資金供与に特化した犯罪類型",
            "D. 不正収益を生み出す元となる犯罪行為"
        ],
        "answer": 3,
        "explanation": "前提犯罪（Predicate Offense）とは、マネー・ローンダリングの対象となる不正収益（illicit proceeds）を生み出す元の犯罪行為を指します。麻薬取引、詐欺、横領、贈収賄などが含まれます。FATFは各国に対し、広範な前提犯罪を指定することを勧告しています。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": ["std-ch1-005"]
    },
    {
        "id": "cams-d1-005",
        "question": "生命保険を悪用したマネー・ローンダリングの手口として最も典型的なものはどれか。",
        "questionEn": "Which is the most classic example of a money laundering scheme involving life insurance?",
        "options": [
            "A. 保険料を少額ずつ複数の口座から支払う",
            "B. 保険金受取人を頻繁に変更する",
            "C. フリールック期間（クーリングオフ）を利用し、一括払い後に全額返金を受けるスキーム",
            "D. 偽の死亡届を提出して保険金を詐取する"
        ],
        "answer": 2,
        "explanation": "フリールック期間（Free-look period）を悪用したローンダリングは、犯罪収益で生命保険に一括加入し、クーリングオフ期間内に解約して全額返金を受ける古典的手口です。返金された資金は保険会社からの正当な支払いとして見えるため、資金洗浄が完了します。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    # ---- Deck 02 (Q6-Q10) ----
    {
        "id": "cams-d1-006",
        "question": "ファントムシッピング（Phantom Shipping）による貿易ベースの資金洗浄において、荷物の写真が提供された場合、最も適切な対応はどれか。",
        "questionEn": "In a phantom shipping TBML scenario, if a photo of cargo is provided as proof, what is the most appropriate response?",
        "options": [
            "A. 写真があれば貨物の存在を確認できたとみなす",
            "B. 写真では何も証明できず、独立した第三者による検証が必要である",
            "C. 写真を警察に提出する",
            "D. 輸出者のウェブサイトで商品を確認する"
        ],
        "answer": 1,
        "explanation": "ファントムシッピングでは実際には貨物が存在しないため、写真だけでは貨物の存在を証明できません。独立した第三者（検査会社、税関等）による実地検証が必要です。TBMLでは書類の偽造が容易であり、独立した検証（independent verification）が不可欠です。",
        "tags": ["tbml"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-007",
        "question": "ローンを利用したマネー・ローンダリングの手口として最も該当するものはどれか。",
        "questionEn": "Which of the following best describes a money laundering method involving loans?",
        "options": [
            "A. 汚れた資金でローンを期限前に一括返済する",
            "B. 合法的な収入でローンを組み、計画的に返済する",
            "C. 複数の金融機関でローンの借り換えを繰り返す",
            "D. 事業拡大のために設備投資ローンを利用する"
        ],
        "answer": 0,
        "explanation": "犯罪収益を正当に見せかけるため、まず合法的にローンを組み、その後犯罪収益（dirty cash）でローンを期限前に一括返済する手口があります。返済後の資産はローンで購入した正当なものとして見えるため、資金洗浄が達成されます。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-008",
        "question": "ある金属スクラップ業者が大量の現金取引を行い、実態以上の売上を計上している。この業者の最も適切な分類はどれか。",
        "questionEn": "A scrap metal business conducts large cash transactions and reports revenue exceeding its actual operations. How is this business best classified?",
        "options": [
            "A. 高リスク顧客（High-Risk Customer）",
            "B. フロント企業（Front/Shell Company）",
            "C. 合法的な現金集約型ビジネス",
            "D. 特別目的事業体（SPV）"
        ],
        "answer": 1,
        "explanation": "実態以上の売上を計上し、大量の現金取引を行う業者は、犯罪収益を正当な事業収入に見せかけるフロント企業（Front Company）またはシェルカンパニーと分類されます。現金集約型ビジネスは資金洗浄に悪用されやすく、実態との乖離が重要な指標となります。",
        "tags": ["ml-basics", "corporate-vehicles"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-009",
        "question": "預金取扱金融機関における規制上の疑わしい取引指標（Red Flag）として最も該当するものはどれか。",
        "questionEn": "Which of the following is the most relevant regulatory red flag for a deposit-taking institution?",
        "options": [
            "A. 顧客が毎月同額の家賃を振り込む",
            "B. 学生口座での少額のオンライン購入",
            "C. 単一の受取人宛に大量の国内電信送金を行うこと",
            "D. 季節変動に応じた小売業者の売上入金"
        ],
        "answer": 2,
        "explanation": "単一の受取人宛に大量の国内電信送金（high volume domestic wires to single beneficiary）を行うことは、ファネルアカウントやストラクチャリングに関連する典型的な疑わしい取引指標です。正当なビジネスの理由なく特定の口座に集中的に送金されるパターンは、資金集約型の洗浄手法を示唆します。",
        "tags": ["monitoring", "sar"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-010",
        "question": "カジノにおけるストラクチャリングの疑わしい取引指標として最も該当するものはどれか。",
        "questionEn": "Which scenario is most indicative of structuring at a casino?",
        "options": [
            "A. VIP顧客がクレジットラインで$100,000のチップを購入する",
            "B. 顧客がスロットマシンで一晩に$15,000を使う",
            "C. 観光客がチップを$500分購入してポーカーをプレイする",
            "D. 顧客が同日に$2,900ずつ2回現金に換金する"
        ],
        "answer": 3,
        "explanation": "報告閾値（$3,000や$10,000）を回避するために取引を分割することがストラクチャリングです。$2,900ずつ2回（合計$5,800）の換金は、$3,000のカジノ報告閾値を意図的に回避する典型的なストラクチャリングのパターンです。",
        "tags": ["casino", "ml-basics"],
        "relatedJpQuestions": []
    },
    # ---- Deck 03 (Q11-Q15) ----
    {
        "id": "cams-d1-011",
        "question": "コルレス銀行に対するデューデリジェンスで最低限必要な事項はどれか。",
        "questionEn": "What is the minimum due diligence requirement for correspondent banking relationships?",
        "options": [
            "A. シェルバンクでないことの確認、実質的所有者の特定、AML管理体制の確認",
            "B. コルレス銀行の全顧客リストの取得",
            "C. コルレス銀行の全取引のリアルタイム監視",
            "D. コルレス銀行の内部監査報告書の閲覧"
        ],
        "answer": 0,
        "explanation": "コルレス銀行との関係構築にあたっては、最低限、シェルバンクでないことの確認、実質的所有者（UBO）の特定、AML/CFT管理体制の評価が求められます。これはFATF勧告13およびウォルフスバーグ・コルレス銀行原則に基づく要件です。",
        "tags": ["correspondent", "cdd"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-012",
        "question": "PTA（Payable-Through Account）に関するリスクとして最も適切なものはどれか。",
        "questionEn": "What is the primary risk associated with Payable-Through Accounts (PTAs)?",
        "options": [
            "A. PTAでは手数料が過剰に課される可能性がある",
            "B. 米国の銀行がサブアカウントの保有者を把握できない可能性がある",
            "C. PTAは国内送金にのみ使用される",
            "D. PTAは中央銀行によって直接監督される"
        ],
        "answer": 1,
        "explanation": "PTA（Payable-Through Account）では、海外のレスポンデント銀行の顧客が米国銀行のシステムを通じて直接取引を行えるため、米国の銀行がサブアカウント保有者の身元を把握できないリスクがあります。これはネスティッドに類似したリスクを生じさせます。",
        "tags": ["correspondent"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-013",
        "question": "プライベートバンキングにおいてPEP顧客に対するEDD（強化された顧客管理）として最も適切な措置の組み合わせはどれか。",
        "questionEn": "Which combination of measures constitutes appropriate EDD for a PEP in private banking?",
        "options": [
            "A. 年1回の書面審査のみ",
            "B. 通常のCDDに加え口座残高の上限設定",
            "C. 上級管理職の承認、資金源（SoF）および資産源（SoW）の確認、継続的な強化モニタリング",
            "D. PEP顧客との取引を一律に拒否する"
        ],
        "answer": 2,
        "explanation": "プライベートバンキングにおけるPEPへのEDDには、上級管理職（Senior Management）の承認、資金源（Source of Funds）と資産源（Source of Wealth）の詳細な確認、および継続的な強化モニタリングが含まれます。これはFATF勧告12およびウォルフスバーグPB原則に基づきます。",
        "tags": ["pep", "edd"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-014",
        "question": "31 USC §5324に基づくストラクチャリングについて、正しい記述はどれか。",
        "questionEn": "Under 31 USC §5324, which statement about structuring is correct?",
        "options": [
            "A. ストラクチャリングは$10,000超の取引にのみ適用される",
            "B. ストラクチャリングの意図があってもCTRが提出されれば違法ではない",
            "C. ストラクチャリングは民事違反のみで刑事罰の対象ではない",
            "D. CTRの提出有無にかかわらずSARの提出が必要であり、ストラクチャリングの意図自体が違法である"
        ],
        "answer": 3,
        "explanation": "31 USC §5324に基づき、報告要件を回避する意図でのストラクチャリングはそれ自体が連邦犯罪です。CTRが結果的に提出されたかどうかは関係なく、SARの提出が必要です。金額が$10,000未満であっても、報告回避の意図があれば違法となります。",
        "tags": ["us-law", "sar"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-015",
        "question": "ネスティッド・コルレスバンキング（Nested Correspondent Banking）に対する最も適切な対応はどれか。",
        "questionEn": "What is the most appropriate response to nested correspondent banking?",
        "options": [
            "A. ネスティングを完全に禁止する",
            "B. レスポンデント銀行の顧客リストを直接取得する",
            "C. 下流の金融機関（downstream institutions）に関する情報を取得する",
            "D. すべてのコルレス関係を解消する"
        ],
        "answer": 2,
        "explanation": "ネスティッドでは、レスポンデント銀行が自らのコルレス口座を通じて、さらに他の金融機関（downstream institutions）にアクセスを提供します。この場合、コルレス銀行は下流の金融機関に関する情報（AML体制、規制状況等）を取得し、リスクを評価する必要があります。",
        "tags": ["correspondent"],
        "relatedJpQuestions": []
    },
    # ---- Deck 04 (Q16-Q20) ----
    {
        "id": "cams-d1-016",
        "question": "MSB（Money Service Business）のスーパーエージェントに関するリスクとして最も重要なものはどれか。",
        "questionEn": "What is the most significant risk associated with MSB super agents?",
        "options": [
            "A. スーパーエージェントは送金手数料を過剰に課す可能性がある",
            "B. スーパーエージェントが資金洗浄に加担（complicit）している可能性がある",
            "C. スーパーエージェントはライセンスが不要である",
            "D. スーパーエージェントは国際送金ができない"
        ],
        "answer": 1,
        "explanation": "MSBのスーパーエージェントは、大量の取引を処理する立場にあり、犯罪者と共謀して資金洗浄に加担（complicit）するリスクがあります。エージェントの監督と管理はMSBのAMLプログラムの重要な要素であり、定期的なモニタリングと研修が必要です。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-017",
        "question": "貴金属・宝石取引における疑わしい取引指標として最も該当するものはどれか。",
        "questionEn": "Which is the most relevant red flag in a precious metals and stones transaction?",
        "options": [
            "A. 顧客が宝石の鑑定書を要求する",
            "B. 貴金属ディーラーが取引記録を保管する",
            "C. 顧客が交渉なく市場価格を上回る金額で支払う",
            "D. 顧客が複数の宝石店を比較検討する"
        ],
        "answer": 2,
        "explanation": "交渉なく市場価格を上回る金額で支払うことは、典型的な資金洗浄の指標です。通常の商取引では価格交渉が行われますが、資金洗浄が目的の場合、犯罪者は迅速に大量の現金を処分するため、価格に無頓着になる傾向があります。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-018",
        "question": "カジノにおけるチップダンピング（Chip Dumping）の特徴として最も適切なものはどれか。",
        "questionEn": "What is the primary characteristic of chip dumping at a casino?",
        "options": [
            "A. 記録を残さずにレイヤリング（階層化）を促進する",
            "B. カジノの売上を増加させる正当な行為である",
            "C. チップを購入せずにゲームに参加する行為",
            "D. カジノ従業員にチップを渡す一般的なチップ習慣"
        ],
        "answer": 0,
        "explanation": "チップダンピングとは、故意にポーカー等のゲームで負けることで、共犯者にチップを移転する手法です。これにより、取引の記録を残さずに資金の移転（レイヤリング）が可能になります。カジノ内の監視カメラでは通常のゲームプレイと区別が困難です。",
        "tags": ["casino", "ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-019",
        "question": "カジノを利用したマネー・ローンダリングの最も一般的な手口はどれか。",
        "questionEn": "What is the most common method of money laundering through a casino?",
        "options": [
            "A. スロットマシンで長時間プレイして勝利金を得る",
            "B. カジノの株式を購入する",
            "C. 現金でチップを購入し、ほとんどプレイせずにチップを小切手に換金する",
            "D. カジノの会員カードにポイントを蓄積する"
        ],
        "answer": 2,
        "explanation": "最も一般的なカジノでのマネー・ローンダリングは、犯罪収益の現金でチップを購入し、最小限のプレイの後、チップをカジノ発行の小切手に換金する手口です。小切手はカジノという正当な企業からの支払いとして見えるため、資金の出所が隠蔽されます。",
        "tags": ["casino", "ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-020",
        "question": "不動産取引において、第三者が資金提供者に代わって物件を購入する役割を果たした人物は、AML/CFTの観点から最も適切にどのように分類されるか。",
        "questionEn": "In a real estate transaction where a third party purchases property on behalf of a funds provider, how is that person best classified from an AML/CFT perspective?",
        "options": [
            "A. 正当な代理人（Legitimate Agent）",
            "B. マネーミュール（Money Mule）としてプレースメントの門番の役割を果たした",
            "C. 不動産ブローカー",
            "D. 無関係の第三者"
        ],
        "answer": 1,
        "explanation": "犯罪収益の提供者に代わって不動産を購入する第三者は、マネーミュール（Money Mule）として機能し、プレースメント（配置）段階のゲートキーパーの役割を果たしています。不動産は高額で、所有権の移転により資金の出所を隠蔽できるため、資金洗浄に多用されます。",
        "tags": ["real-estate", "ml-basics"],
        "relatedJpQuestions": []
    },
    # ---- Deck 05 (Q21-Q25) ----
    {
        "id": "cams-d1-021",
        "question": "TBML（Trade-Based Money Laundering：貿易ベースの資金洗浄）の定義として最も適切なものはどれか。",
        "questionEn": "What is the best definition of Trade-Based Money Laundering (TBML)?",
        "options": [
            "A. 合法的な貿易を通じて利益を最大化する行為",
            "B. 貿易取引を偽装・操作して犯罪収益を移転・隠蔽する行為",
            "C. 自由貿易協定を悪用する行為",
            "D. 輸出入品に対する関税の回避"
        ],
        "answer": 1,
        "explanation": "TBMLとは、貿易取引を偽装または操作することにより、犯罪収益の移転や隠蔽を行う手法です。過大・過少インボイス（Over/Under-invoicing）、ファントムシッピング（架空貨物）、複数請求（Multiple invoicing）などの手口が含まれます。",
        "tags": ["tbml"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-022",
        "question": "ファネルアカウント（Funnel Account）の特徴として最も適切なものはどれか。",
        "questionEn": "What is the primary feature of a funnel account?",
        "options": [
            "A. 複数の地域で入金が行われ、別の地域でまとめて出金される",
            "B. 単一の口座に定期的な給与が入金される",
            "C. 海外送金専用の口座",
            "D. 投資目的の信託口座"
        ],
        "answer": 0,
        "explanation": "ファネルアカウント（漏斗口座）は、複数の地理的場所で現金が入金され、別の単一の場所（多くの場合、国境近くや国外）でまとめて引き出される口座です。麻薬収益の本国送金などに多用され、口座の地理的利用パターンが異常な指標となります。",
        "tags": ["ml-basics", "monitoring"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-023",
        "question": "サイバー犯罪関連の疑わしい取引指標（Red Flag）として最も該当するものはどれか。",
        "questionEn": "Which is the most relevant red flag for cybercrime-related money laundering?",
        "options": [
            "A. 顧客がオンラインバンキングを利用している",
            "B. 既知のランサムウェアやダークネット関連のウォレットとの取引がある",
            "C. 顧客が複数のメールアドレスを保有している",
            "D. 顧客がVPNを使用してログインしている"
        ],
        "answer": 1,
        "explanation": "既知のランサムウェアやダークネットマーケット関連のウォレットアドレスとの暗号資産取引は、サイバー犯罪に関連する最も明確な疑わしい取引指標です。ブロックチェーン分析ツールにより、こうした高リスクアドレスとの関連を検知することが可能です。",
        "tags": ["crypto", "monitoring"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-024",
        "question": "プリペイドカードに関するAML/CFTリスクとして最も重要な懸念はどれか。",
        "questionEn": "What is the most significant AML/CFT concern regarding prepaid cards?",
        "options": [
            "A. プリペイドカードの残高が低すぎること",
            "B. プリペイドカードの有効期限が短いこと",
            "C. 国境を越えた価値の移転が可能であること",
            "D. プリペイドカードの利用手数料が高いこと"
        ],
        "answer": 2,
        "explanation": "プリペイドカードの最大のAML/CFTリスクは、匿名で国境を越えた価値の移転（cross-border movement of value）が可能であることです。物理的な現金の移動なく国際的な資金移転が行えるため、税関での検知が困難です。",
        "tags": ["ml-basics"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-025",
        "question": "不動産取引における以下の状況のうち、マネー・ローンダリングの疑わしい取引指標として最も可能性が低いものはどれか。",
        "questionEn": "Which of the following real estate scenarios is LEAST likely to be a red flag for money laundering?",
        "options": [
            "A. 不動産をすぐに転売し、利益を異なる口座に分散させる",
            "B. 法人名義で高額物件を購入し、実質的所有者が不明",
            "C. 不動産の購入価格が市場価格を大幅に上回る",
            "D. 需要の高い都市部でのアパート取得"
        ],
        "answer": 3,
        "explanation": "需要の高い都市部でのアパート取得は、一般的な不動産投資行動であり、それ自体がマネー・ローンダリングの疑わしい取引指標とはなりません。一方、迅速な転売、不明確な所有構造、市場価格を逸脱した取引は典型的な疑わしい指標です。",
        "tags": ["real-estate"],
        "relatedJpQuestions": []
    },
    # ---- Deck 06 (Q26-Q30) ----
    {
        "id": "cams-d1-026",
        "question": "シェルフカンパニー（Shelf Company）の特徴として最も適切なものはどれか。",
        "questionEn": "What best describes a shelf company and how it differs from a shell company?",
        "options": [
            "A. 設立直後に事業を開始した法人",
            "B. 犯罪収益を隠すために新たに設立されたペーパーカンパニー",
            "C. 数年前に設立され、経年させるために休眠状態で維持されていた法人",
            "D. 上場企業の完全子会社"
        ],
        "answer": 2,
        "explanation": "シェルフカンパニー（Shelf Company = 「棚に置かれた会社」）は、将来の販売目的で設立され、事業活動を行わずに数年間休眠状態で維持（aged）された法人です。設立年数が古いため信頼性があるように見え、資金洗浄の隠れ蓑として悪用されることがあります。シェルカンパニーとは異なり、意図的に「熟成」されている点が特徴です。",
        "tags": ["corporate-vehicles"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-027",
        "question": "シェルバンク（Shell Bank）の定義として正しいものはどれか。",
        "questionEn": "What is the correct definition of a shell bank?",
        "options": [
            "A. オンラインバンキングのみを提供する銀行",
            "B. 物理的な拠点を持たず、規制を受ける金融グループに所属していない銀行",
            "C. 中央銀行の子会社",
            "D. 破産手続き中の銀行"
        ],
        "answer": 1,
        "explanation": "シェルバンク（Shell Bank）とは、設立国に物理的な拠点（physical presence）を持たず、規制された金融グループにも所属していない銀行です。FATF勧告13により、金融機関はシェルバンクとのコルレス関係を禁止されており、レスポンデント銀行がシェルバンクでないことを確認する義務があります。",
        "tags": ["corporate-vehicles", "correspondent"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-028",
        "question": "クック諸島のトラストに「強迫条項（Duress Clause）」が含まれている場合、その主な目的は何か。",
        "questionEn": "What is the primary purpose of a Duress Clause in a Cook Islands trust?",
        "options": [
            "A. 受託者に投資裁量を与えること",
            "B. 信託を慈善目的に限定すること",
            "C. 受益者を秘匿すること",
            "D. 資産保護（Asset Protection）"
        ],
        "answer": 3,
        "explanation": "クック諸島のトラストの強迫条項（Duress Clause）は、設定者が外国の裁判所から強制される場合に、受託者が当該命令に従う義務を免除する条項です。これにより、外国の債権者や法執行機関からの資産没収・差押えを困難にし、資産保護（Asset Protection）を目的としています。",
        "tags": ["corporate-vehicles"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-029",
        "question": "ノミニーディレクター（Nominee Director）の役割として最も適切なものはどれか。",
        "questionEn": "What is the primary role of a nominee director from an AML/CFT perspective?",
        "options": [
            "A. 会社の日常業務を管理する経営者",
            "B. 実質的所有者（UBO）の身元を隠すためのストローマン（名義人）",
            "C. 外部監査を実施する独立した第三者",
            "D. 規制当局との連絡窓口"
        ],
        "answer": 1,
        "explanation": "ノミニーディレクター（名義取締役）は、法人登記上の取締役として名前を貸すことで、実質的所有者（UBO）の身元を隠蔽するストローマン（straw man）として機能します。これにより、法人の背後にいる真の支配者を特定することが困難になり、マネー・ローンダリングのリスクが高まります。",
        "tags": ["corporate-vehicles", "ubo"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-030",
        "question": "無記名株式（Bearer Shares）の最大のリスクは何か。",
        "questionEn": "What is the primary risk associated with bearer shares?",
        "options": [
            "A. 所有権が匿名で移転可能であること",
            "B. 株式の価値が不安定であること",
            "C. 配当金の支払いが困難であること",
            "D. 発行コストが高額であること"
        ],
        "answer": 0,
        "explanation": "無記名株式（Bearer Shares）の最大のリスクは、株券の物理的な引渡しのみで所有権が匿名で移転できる点です。株主名簿への登録が不要なため、法人の実質的所有者を特定することが極めて困難になります。多くの国がこの問題に対応するため、無記名株式を廃止または厳格に規制しています。",
        "tags": ["corporate-vehicles", "ubo"],
        "relatedJpQuestions": []
    },
    # ---- Deck 07 (Q31-Q35) ----
    {
        "id": "cams-d1-031",
        "question": "テロ資金供与（TF）の検知がマネー・ローンダリング（ML）の検知と比べて困難である主な理由はどれか。",
        "questionEn": "What is the primary challenge in detecting terrorist financing (TF) compared to money laundering (ML)?",
        "options": [
            "A. テロ資金は合法的な資金源から供給される可能性があり、少額であることが多い",
            "B. テロ資金は常に大口現金取引として行われる",
            "C. テロ資金供与は国際送金のみで行われる",
            "D. テロ資金供与はMLと同じ手法のみで行われる"
        ],
        "answer": 0,
        "explanation": "テロ資金供与がMLと比べて検知が困難な主な理由は、テロ資金が合法的な資金源（寄付、事業収入、給与等）から供給される可能性があり、かつ個々の取引が少額（small amounts）であることが多いためです。MLは犯罪収益の洗浄が前提ですが、TFでは資金自体が合法的である場合があります。",
        "tags": ["tf"],
        "relatedJpQuestions": ["std-ch1-004"]
    },
    {
        "id": "cams-d1-032",
        "question": "FATF勧告8におけるNPO（非営利団体）への対応として最も適切なアプローチはどれか。",
        "questionEn": "What is the most appropriate approach to NPOs under FATF Recommendation 8?",
        "options": [
            "A. すべてのNPOに対して同一の厳格な規制を適用する",
            "B. リスクベースで対象を絞り、合法的なNPO活動を阻害しない対応",
            "C. NPOの国際活動を全面的に禁止する",
            "D. NPOをすべて金融機関と同じ規制下に置く"
        ],
        "answer": 1,
        "explanation": "FATF勧告8は、NPOに対してリスクベースで対象を絞った（targeted）アプローチを求めており、テロ資金供与に悪用されるリスクのあるNPOを特定しつつ、合法的な慈善活動（legitimate charitable activity）を阻害しないよう求めています。過度な規制はNPOの活動を萎縮させる恐れがあります。",
        "tags": ["tf", "fatf", "rba"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-033",
        "question": "FATF勧告1の主な内容はどれか。",
        "questionEn": "What is the primary content of FATF Recommendation 1?",
        "options": [
            "A. 顧客管理（CDD）の実施基準",
            "B. 疑わしい取引の届出義務",
            "C. 国際協力の枠組み",
            "D. リスクの評価とリスクベース・アプローチ（RBA）の適用"
        ],
        "answer": 3,
        "explanation": "FATF勧告1は、各国および金融機関に対し、ML/TFリスクを特定・評価・理解し、それに応じたリスクベース・アプローチ（RBA）を適用することを求めています。RBAはFATF勧告体系の基盤であり、限られたリソースを高リスク分野に集中的に配分することを目的としています。",
        "tags": ["fatf", "rba"],
        "relatedJpQuestions": ["std-ch2-001"]
    },
    {
        "id": "cams-d1-034",
        "question": "国連安全保障理事会決議（UNSCR）1267に基づく資産凍結について、正しい記述はどれか。",
        "questionEn": "Which statement correctly describes asset freezing under UNSCR 1267?",
        "options": [
            "A. 各国が独自にリストを作成し、任意に適用する",
            "B. 資産凍結は金融機関の裁量で行われる",
            "C. 国連統合リストに基づく拘束力のある義務として各国に適用される",
            "D. 資産凍結は一定期間後に自動的に解除される"
        ],
        "answer": 2,
        "explanation": "UNSCR 1267は、アルカイダ、ISIL等に関連する個人・団体の資産凍結を全UN加盟国に義務付ける決議です。国連統合リスト（Consolidated UN List）に基づき、各国は拘束力のある（binding）義務として遅滞なく資産凍結を実施しなければなりません。",
        "tags": ["sanctions", "tf"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d1-035",
        "question": "FATFの旧特別勧告VI（ハワラ等の代替送金サービス）は、現在のFATF勧告のどこに統合されているか。",
        "questionEn": "Where has the former FATF Special Recommendation VI (on hawala and alternative remittance) been incorporated in the current FATF Recommendations?",
        "options": [
            "A. 勧告10（顧客管理）",
            "B. 勧告16（電信送金）",
            "C. 勧告14（MVTS登録・認可制度）",
            "D. 勧告20（疑わしい取引の届出）"
        ],
        "answer": 2,
        "explanation": "旧特別勧告VI（ハワラ等の代替送金サービス）は、現在のFATF勧告14に統合されています。勧告14は、MVTS（Money or Value Transfer Services）事業者に対する登録・認可制度（licensing）を求め、無登録のMVTS運営を犯罪として取り扱うことを規定しています。",
        "tags": ["fatf"],
        "relatedJpQuestions": []
    },
]

# ---------------------------------------------------------------------------
# Domain 2: Compliance Standards  (Q36-Q50)
# ---------------------------------------------------------------------------
domain2_questions = [
    # ---- Deck 08 (Q36-Q40) ----
    {
        "id": "cams-d2-001",
        "question": "コルレス銀行が自行のPEPリストの提供を求めてきたが、GDPR上の理由でリスト全体の共有を拒否する必要がある場合、最も適切な対応はどれか。",
        "questionEn": "A correspondent bank requests your PEP list, but GDPR prevents sharing the full list. What is the most appropriate response?",
        "options": [
            "A. リストの全体をそのまま提供する",
            "B. リクエストを完全に拒否する",
            "C. PEPリストではなく、自行のPEPスクリーニングプロセスについて説明する",
            "D. リストを暗号化して送信する"
        ],
        "answer": 2,
        "explanation": "GDPRの制約によりPEPリスト全体の共有は困難ですが、完全な拒否もコルレス関係に悪影響を与えます。最適なアプローチは、自行がどのようなPEPスクリーニングプロセスを運用しているかを説明し、リストの代わりにプロセスの健全性を示すことです。",
        "tags": ["correspondent", "privacy-law", "pep"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-002",
        "question": "FSRB（FATF-Style Regional Bodies）とFATFの関係として最も適切なものはどれか。",
        "questionEn": "What best describes the relationship between FSRBs and FATF?",
        "options": [
            "A. FSRBはFATFの下部組織であり、FATFの指示に従う義務がある",
            "B. FSRBはFATFと競合する独立した基準設定機関である",
            "C. FSRBはFATFとは無関係の地域開発銀行のネットワークである",
            "D. FSRBは地域レベルでのFATF基準の遵守を評価・支援する機関である"
        ],
        "answer": 3,
        "explanation": "FSRB（FATF型地域体）は、APG（アジア太平洋グループ）やMONEYVAL等のように、地域レベルでFATF基準の遵守を相互審査により評価し、加盟国の能力向上を支援する機関です。FATFの下部組織ではなく、独立した地域機関としてFATFを支援しています。",
        "tags": ["fatf", "international-cooperation"],
        "relatedJpQuestions": ["std-ch2-001"]
    },
    {
        "id": "cams-d2-003",
        "question": "バーゼル銀行監督委員会（Basel Committee on Banking Supervision）の役割として最も適切なものはどれか。",
        "questionEn": "What best describes the role of the Basel Committee on Banking Supervision?",
        "options": [
            "A. 銀行監督に関するグローバルな基準設定機関",
            "B. 各国の中央銀行の金融政策を調整する機関",
            "C. 国際送金の清算・決済を行う機関",
            "D. 預金保険制度を運営する国際機関"
        ],
        "answer": 0,
        "explanation": "バーゼル銀行監督委員会（BCBS）は、銀行の健全性規制・監督に関するグローバルな基準設定機関です。自己資本比率規制（バーゼルIII）やKYC/AMLに関するガイダンスを策定しており、各国の銀行監督当局の協力を促進しています。",
        "tags": ["international-cooperation", "governance"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-004",
        "question": "ウォルフスバーグ・グループ（Wolfsberg Group）の説明として最も適切なものはどれか。",
        "questionEn": "Which best describes the Wolfsberg Group?",
        "options": [
            "A. FATF加盟国の財務省のネットワーク",
            "B. マネー・ローンダリング対策を専門とする国際刑事警察機構の部門",
            "C. 主要国の金融規制当局の連合体",
            "D. 金融犯罪リスクの枠組み策定のために連携するグローバル銀行の団体"
        ],
        "answer": 3,
        "explanation": "ウォルフスバーグ・グループは、13の主要グローバル銀行（Deutsche Bank、HSBC、JPMorgan等）で構成される民間の団体であり、AML/CFTおよび金融犯罪リスクに関する業界ガイダンスや原則（コルレス銀行原則、プライベートバンキング原則等）を策定しています。",
        "tags": ["international-cooperation"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-005",
        "question": "エグモント・グループ（Egmont Group）の説明として最も適切なものはどれか。",
        "questionEn": "What best describes the Egmont Group?",
        "options": [
            "A. 国際的な法執行機関のネットワーク",
            "B. 各国のFIU（金融情報機関）の非公式ネットワーク",
            "C. 国際通貨基金（IMF）の下部組織",
            "D. 暗号資産取引所の業界団体"
        ],
        "answer": 1,
        "explanation": "エグモント・グループは、各国の金融情報機関（FIU：Financial Intelligence Unit）の非公式な（informal）国際ネットワークです。加盟FIU間での情報交換を促進し、FIUの能力向上を支援しています。現在160以上のFIUが加盟しています。",
        "tags": ["international-cooperation", "sar"],
        "relatedJpQuestions": []
    },
    # ---- Deck 09 (Q41-Q45) ----
    {
        "id": "cams-d2-006",
        "question": "EUのUBO（実質的所有者）登記簿について、2022年のEU司法裁判所（CJEU）判決後の状況として最も適切なものはどれか。",
        "questionEn": "What is the current status of EU UBO registers following the 2022 CJEU ruling?",
        "options": [
            "A. UBO登記簿は完全に廃止された",
            "B. UBO登記簿は引き続き一般公開されている",
            "C. 正当な利益（Legitimate Interest）に基づくアクセス枠組みに移行した",
            "D. UBO登記簿は法執行機関のみがアクセス可能になった"
        ],
        "answer": 2,
        "explanation": "2022年のEU司法裁判所（CJEU）判決（Joined Cases C-37/20 and C-601/20）により、5AMLDで導入されたUBO登記簿の一般公開規定はプライバシー権侵害として無効とされました。これを受け、各加盟国は正当な利益（Legitimate Interest）を証明した者にのみアクセスを認める枠組みに移行しています。",
        "tags": ["eu-amld", "ubo", "privacy-law"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-007",
        "question": "EU第6次マネー・ローンダリング指令（6AMLD）における刑事責任の拡大として正しいものはどれか。",
        "questionEn": "What is a key expansion of criminal liability under the EU 6th Anti-Money Laundering Directive (6AMLD)?",
        "options": [
            "A. 法人への刑事責任の適用および幇助・教唆（Aiding and Abetting）の犯罪化",
            "B. 金融機関の従業員個人への民事責任の免除",
            "C. 前提犯罪の範囲の縮小",
            "D. 自己資金洗浄（Self-Laundering）の除外"
        ],
        "answer": 0,
        "explanation": "6AMLDは、法人（Legal Persons）への刑事責任の適用を明確化し、マネー・ローンダリングの幇助・教唆（Aiding and Abetting）も犯罪として処罰対象に加えました。また、自己資金洗浄（Self-Laundering）の犯罪化や、前提犯罪の統一リスト（22犯罪類型）の策定も含まれています。",
        "tags": ["eu-amld"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-008",
        "question": "EU第5次マネー・ローンダリング指令（5AMLD）で新たに規制対象に追加されたセクターはどれか。",
        "questionEn": "Which sector was newly brought under regulation by the EU 5th Anti-Money Laundering Directive (5AMLD)?",
        "options": [
            "A. 暗号資産交換業者およびカストディアルウォレットプロバイダー",
            "B. 不動産仲介業者",
            "C. 弁護士・公証人",
            "D. 貴金属取扱業者"
        ],
        "answer": 0,
        "explanation": "5AMLD（2018年）は、暗号資産交換業者（Virtual Currency Exchange Providers）およびカストディアルウォレットプロバイダー（Custodian Wallet Providers）を初めてAML/CFT規制の対象に加えました。これは暗号資産の匿名性がもたらすML/TFリスクへの対応です。",
        "tags": ["eu-amld", "crypto"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-009",
        "question": "5AMLDにおけるプリペイドカードに関する変更点として正しいものはどれか。",
        "questionEn": "What change did 5AMLD introduce regarding prepaid cards?",
        "options": [
            "A. プリペイドカードの使用を全面禁止した",
            "B. 匿名利用可能な上限額を€250から€150に引き下げた",
            "C. プリペイドカードの発行をEU域内に限定した",
            "D. プリペイドカードに対する新たな税制を導入した"
        ],
        "answer": 1,
        "explanation": "5AMLDは、匿名で利用可能なプリペイドカードの上限額を€250から€150に引き下げました（遠隔支払いの場合は€50）。また、EU域外で発行されたプリペイドカードのEU域内での使用にもCDD要件を適用しています。",
        "tags": ["eu-amld"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-010",
        "question": "米国愛国者法（USA PATRIOT Act）第311条の規定として正しいものはどれか。",
        "questionEn": "What does Section 311 of the USA PATRIOT Act authorize?",
        "options": [
            "A. すべての金融機関にCTR提出を義務付ける",
            "B. 財務省に対し、主要なマネー・ローンダリング懸念先（Primary Money Laundering Concern）を指定する権限を付与する",
            "C. 金融機関にすべての国際送金を停止する権限を与える",
            "D. FBIに金融機関の直接監査権限を付与する"
        ],
        "answer": 1,
        "explanation": "USA PATRIOT Act §311は、米国財務省（FinCEN）に対し、外国の法域、金融機関、または取引類型を「主要なマネー・ローンダリング懸念先」（Primary Money Laundering Concern）に指定し、特別措置（Special Measures）を課す権限を付与しています。",
        "tags": ["us-law"],
        "relatedJpQuestions": []
    },
    # ---- Deck 10 (Q46-Q50) ----
    {
        "id": "cams-d2-011",
        "question": "OFAC（米国財務省外国資産管理室）の域外適用（Extraterritorial Reach）について、正しい記述はどれか。",
        "questionEn": "What correctly describes OFAC's extraterritorial reach?",
        "options": [
            "A. 制裁対象との無許可取引を禁止し、米ドル取引を通じて非米国企業にも適用される",
            "B. OFACの管轄は米国内の金融機関に限定される",
            "C. 域外適用は国連決議に基づく場合にのみ適用される",
            "D. 非米国企業がOFAC規制に違反しても罰則はない"
        ],
        "answer": 0,
        "explanation": "OFACの制裁プログラムは域外適用があり、米ドル建て取引を行うすべての金融機関（非米国企業を含む）に対し、制裁対象（SDNリスト等）との無許可取引（unlicensed transactions）を禁止しています。米ドルクリアリングを通じて事実上グローバルに適用されます。",
        "tags": ["sanctions", "us-law"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-012",
        "question": "OFACのSDNリスト（Specially Designated Nationals List）の目的として最も適切なものはどれか。",
        "questionEn": "What is the purpose of OFAC's SDN (Specially Designated Nationals) List?",
        "options": [
            "A. 米国の輸出管理対象品目を特定すること",
            "B. 国際テロ組織のメンバーのみを特定すること",
            "C. 米国の金融システムに参加できる外国銀行を認定すること",
            "D. 取引を禁止すべき個人・団体を特定すること"
        ],
        "answer": 3,
        "explanation": "OFACのSDNリスト（Specially Designated Nationals and Blocked Persons List）は、テロリスト、麻薬取引組織、大量破壊兵器拡散者など、米国が取引を禁止する個人および団体を特定するリストです。SDNの資産は凍結（blocked）され、米国人との取引は原則として禁止されます。",
        "tags": ["sanctions", "us-law", "filtering"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-013",
        "question": "OFACのスクリーニングで「Saddam Husein」というあいまい一致（Fuzzy Match）が検出された場合、最も適切な対応はどれか。",
        "questionEn": "When OFAC screening produces a fuzzy match for 'Saddam Husein,' what is the most appropriate response?",
        "options": [
            "A. 名前が完全一致ではないため、即座にクリアする",
            "B. 自動的に取引を拒否する",
            "C. 生年月日、住所、パスポート番号などの追加情報を用いて徹底的に調査する",
            "D. OFACに直接連絡して確認する"
        ],
        "answer": 2,
        "explanation": "あいまい一致（Fuzzy Match）が検出された場合、スペルの違いだけで判断すべきではありません。生年月日（DOB）、住所、パスポート番号、国籍などの追加識別情報を用いて徹底的に調査（thorough investigation）を行い、真の一致（True Positive）か誤検知（False Positive）かを判定する必要があります。",
        "tags": ["sanctions", "filtering"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-014",
        "question": "リスクベース・アプローチ（RBA）において、取引を一律に禁止すべき顧客カテゴリーはどれか。",
        "questionEn": "Under a risk-based approach, which customer category should be universally prohibited?",
        "options": [
            "A. PEP（重要な公的地位を有する者）",
            "B. シェルバンク（Shell Bank）",
            "C. 現金集約型ビジネス（Cash-Intensive Business）",
            "D. 非居住者（Non-Resident Customer）"
        ],
        "answer": 1,
        "explanation": "シェルバンク（Shell Bank）は、物理的拠点を持たず規制されたグループにも所属しない銀行であり、FATF勧告およびほぼすべての管轄において取引が一律に禁止（prohibited）されています。PEPや現金集約型ビジネスは高リスクですが、EDDにより取引は可能です。",
        "tags": ["rba", "correspondent"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d2-015",
        "question": "新商品・サービスの開発委員会にコンプライアンス・オフィサーが招待された場合、最も適切な対応はどれか。",
        "questionEn": "When the compliance officer is invited to join the new product development committee, what is the most appropriate response?",
        "options": [
            "A. 恒久的なメンバーとして参加することを要請する",
            "B. 新商品の承認後にレビューを行うことを提案する",
            "C. 規制当局に新商品のリスクについて直接相談する",
            "D. 一時的なオブザーバーとして参加する"
        ],
        "answer": 0,
        "explanation": "コンプライアンス・オフィサーは新商品・サービスの開発委員会に恒久的なメンバー（permanent member）として参加すべきです。商品設計段階からML/TFリスクを評価し、適切なリスク軽減策を組み込むことで、事後的な対応よりも効果的にリスクを管理できます。",
        "tags": ["governance"],
        "relatedJpQuestions": []
    },
]

# ---------------------------------------------------------------------------
# Domain 3: AML/CFT Compliance Programme  (Q51-Q70)
# ---------------------------------------------------------------------------
domain3_questions = [
    # ---- Deck 11 (Q51-Q55) ----
    {
        "id": "cams-d3-001",
        "question": "リスクベース・アプローチ（RBA）の基本原則として最も適切なものはどれか。",
        "questionEn": "What is the foundational principle of the Risk-Based Approach (RBA)?",
        "options": [
            "A. すべての顧客に均一な管理措置を適用する",
            "B. リスクの高い顧客との取引を一律に禁止する",
            "C. 規制当局が定めたチェックリストに厳密に従う",
            "D. リスクを特定・評価・理解し、リスクに見合った措置を適用する"
        ],
        "answer": 3,
        "explanation": "RBAの基本原則は、ML/TFリスクを特定（identify）、評価（assess）、理解（understand）し、そのリスクに見合った（commensurate）措置を適用することです。高リスクにはEDD、低リスクにはSDD（Simplified Due Diligence）を適用し、リソースを効率的に配分します。",
        "tags": ["rba"],
        "relatedJpQuestions": ["std-ch4-001"]
    },
    {
        "id": "cams-d3-002",
        "question": "米国のAMLプログラムにおける「第5の柱」（Fifth Pillar）とは何か。",
        "questionEn": "What is the 'Fifth Pillar' of a US AML program?",
        "options": [
            "A. サイバーセキュリティ体制の整備",
            "B. 継続的な顧客管理（Ongoing CDD）手続き",
            "C. 制裁スクリーニングの実施",
            "D. 内部通報制度（ホイッスルブロワー制度）の整備"
        ],
        "answer": 1,
        "explanation": "米国のAMLプログラムの第5の柱（Fifth Pillar）は、2016年のFinCEN CDD最終規則により追加された継続的な顧客管理（Ongoing CDD）手続きです。従来の4つの柱（内部統制、BSAオフィサー、研修、独立テスト）に加え、顧客リスクプロファイルの継続的な更新と監視が義務付けられました。",
        "tags": ["us-law", "cdd", "governance"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-003",
        "question": "BSAオフィサー（BSA/AMLコンプライアンス・オフィサー）の独立性に関する問題として最も適切なものはどれか。",
        "questionEn": "What is the most significant independence concern for a BSA/AML compliance officer?",
        "options": [
            "A. 収益部門との兼務など、利益相反がコンプライアンスの独立性を損なうこと",
            "B. BSAオフィサーが取締役会に直接報告すること",
            "C. BSAオフィサーが外部の研修に参加すること",
            "D. BSAオフィサーが複数の支店を担当すること"
        ],
        "answer": 0,
        "explanation": "BSAオフィサーが収益部門（revenue-generating business lines）と兼務したり、収益目標に連動した評価を受ける場合、利益相反（conflict of interest）が生じ、コンプライアンスの独立性が損なわれます。BSAオフィサーは取引の承認・拒否に関して独立した判断ができる立場にある必要があります。",
        "tags": ["governance", "us-law"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-004",
        "question": "AMLプログラムの独立テスト（Independent Testing）に関する説明として最も適切なものはどれか。",
        "questionEn": "Which statement best describes independent testing of an AML program?",
        "options": [
            "A. 毎月実施し、AML部門の担当者が行うべきである",
            "B. 規制当局の検査をもって独立テストとみなすことができる",
            "C. 12～18ヶ月ごとに、AML機能から独立した有資格者が実施する",
            "D. 独立テストはSAR提出状況のレビューのみで構成される"
        ],
        "answer": 2,
        "explanation": "AMLプログラムの独立テストは、12～18ヶ月ごと（リスクに応じてより頻繁に）に、AML機能から独立した有資格者（qualified personnel independent of the AML function）が実施すべきです。内部監査部門または外部の専門家が適任であり、プログラム全体の有効性を評価します。",
        "tags": ["audit", "governance"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-005",
        "question": "Three Lines Model（3つのディフェンスライン）において、各ラインの役割の対応として正しいものはどれか。",
        "questionEn": "Which correctly maps the Three Lines Model to AML/CFT functions?",
        "options": [
            "A. 第1線＝内部監査、第2線＝営業部門、第3線＝コンプライアンス",
            "B. 第1線＝コンプライアンス、第2線＝営業部門、第3線＝内部監査",
            "C. 第1線＝営業部門（Business）、第2線＝コンプライアンス・リスク管理、第3線＝内部監査",
            "D. 第1線＝取締役会、第2線＝内部監査、第3線＝営業部門"
        ],
        "answer": 2,
        "explanation": "Three Lines Modelでは、第1線＝営業部門（Business Lines）がリスクの所有者として日常的なリスク管理を行い、第2線＝コンプライアンス・リスク管理部門が独立した監視・助言を提供し、第3線＝内部監査が独立した保証（assurance）を提供します。",
        "tags": ["governance"],
        "relatedJpQuestions": []
    },
    # ---- Deck 12 (Q56-Q60) ----
    {
        "id": "cams-d3-006",
        "question": "Three Lines Modelにおいて、コンプライアンス部門が担当するディフェンスラインはどれか。",
        "questionEn": "In the Three Lines Model, which line of defense does the compliance function occupy?",
        "options": [
            "A. 第1線（First Line）",
            "B. 第3線（Third Line）",
            "C. 第2線（Second Line）",
            "D. 取締役会の直轄（Board Direct）"
        ],
        "answer": 2,
        "explanation": "コンプライアンス部門は第2線（Second Line of Defense）に位置します。第1線（営業部門）に対する独立した監視・助言を提供し、ポリシーの策定、リスク評価、モニタリング機能の設計・運営を担います。第3線の内部監査とは異なり、日常的な監視機能を提供します。",
        "tags": ["governance"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-007",
        "question": "非対面での口座開設（Non-Face-to-Face Account Opening）に関する説明として最も適切なものはどれか。",
        "questionEn": "Which statement best describes non-face-to-face account opening?",
        "options": [
            "A. 許容されるがリスクが高いため、追加の本人確認措置が必要",
            "B. すべての法域で禁止されている",
            "C. 対面と同じリスクレベルで処理して問題ない",
            "D. 法人口座にのみ適用される"
        ],
        "answer": 0,
        "explanation": "非対面での口座開設は許容されますが、対面に比べてなりすまし等のリスクが高いため、追加の本人確認措置（additional verification measures）が必要です。電子的本人確認（eKYC）、ビデオ通話、追加書類の提出などが求められます。",
        "tags": ["cdd", "rba"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-008",
        "question": "CAMS試験において、回答に自信がない問題に遭遇した場合の最も効果的な時間管理戦略はどれか。",
        "questionEn": "What is the most effective time management strategy when encountering a question you are unsure about on the CAMS exam?",
        "options": [
            "A. その問題を飛ばして後で戻る",
            "B. 問題を何度も読み直して正解を見つける",
            "C. 最初の直感で回答し、見直さない",
            "D. 時間をかけて消去法で絞り込む"
        ],
        "answer": 0,
        "explanation": "CAMS試験は時間制限があるため、回答に自信がない問題は飛ばして（skip）、他の問題を先に解答した後に戻る戦略が効果的です。すべての問題に均等に時間を配分し、確実に得点できる問題から先に解答することが重要です。",
        "tags": ["training"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-009",
        "question": "コンプライアンス・オフィサー（CO）が法務部長（General Counsel）の直属である場合に生じる問題は何か。",
        "questionEn": "What is the concern when the compliance officer reports to the General Counsel?",
        "options": [
            "A. COの給与が低くなる可能性がある",
            "B. 法務部長がAML/CFTの知識を持っていない可能性がある",
            "C. COが研修プログラムを管理できなくなる",
            "D. COが収益部門から独立している必要があるが、その独立性が確保されない可能性がある"
        ],
        "answer": 3,
        "explanation": "コンプライアンス・オフィサーは収益を生むビジネスライン（revenue business lines）から独立していなければなりません。法務部長が収益部門の業務にも関与している場合、COの独立性が損なわれる可能性があります。理想的にはCOは取締役会またはCEOに直接報告する体制が望ましいです。",
        "tags": ["governance"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-010",
        "question": "CDD（顧客管理）のトリガーイベント（更新契機）として最も適切なものはどれか。",
        "questionEn": "Which is the most appropriate trigger event for updating CDD?",
        "options": [
            "A. 顧客が定期預金の満期を迎えたとき",
            "B. 規制当局が年次報告書を公表したとき",
            "C. 顧客の所有構造、事業内容、またはリスクプロファイルに重大な変更があったとき",
            "D. 金融機関のシステムがアップグレードされたとき"
        ],
        "answer": 2,
        "explanation": "CDDの更新は、顧客の所有構造（ownership）、事業内容（business activities）、またはリスクプロファイル（risk profile）に重大な変更（material change）があった場合にトリガーされます。定期的なレビューに加え、イベントドリブンの更新が重要です。",
        "tags": ["cdd"],
        "relatedJpQuestions": []
    },
    # ---- Deck 13 (Q61-Q65) ----
    {
        "id": "cams-d3-011",
        "question": "バーゼル委員会によるKYC（Know Your Customer）の4つの要素として正しい組み合わせはどれか。",
        "questionEn": "What are the four elements of KYC according to the Basel Committee?",
        "options": [
            "A. 顧客識別（Customer Identification）、リスク管理（Risk Management）、取引モニタリング（Monitoring）、顧客受入方針（Customer Acceptance Policy）",
            "B. 本人確認、住所確認、収入確認、職業確認",
            "C. CDD、EDD、SDD、継続的モニタリング",
            "D. 顧客識別、取引記録保存、SAR提出、制裁スクリーニング"
        ],
        "answer": 0,
        "explanation": "バーゼル委員会のKYCガイダンスは、4つの主要要素として、①顧客受入方針（Customer Acceptance Policy）、②顧客識別（Customer Identification）、③継続的な取引モニタリング（Ongoing Monitoring of Accounts）、④リスク管理（Risk Management）を定めています。",
        "tags": ["cdd", "international-cooperation"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-012",
        "question": "「EDD（強化された顧客管理）はPEPに対してのみ適用すればよい」という記述は正しいか。",
        "questionEn": "Is the statement 'EDD should be applied only to PEPs' correct?",
        "options": [
            "A. 正しい。EDDはPEP専用の措置である",
            "B. 誤り。EDDはPEPに限らず、すべての高リスク顧客に適用される",
            "C. 正しい。ただし家族も含む",
            "D. 場合による。各国の規制次第である"
        ],
        "answer": 1,
        "explanation": "EDD（Enhanced Due Diligence）はPEPに限定されるものではなく、すべての高リスク顧客（high-risk customers）に適用されます。高リスク国との取引、複雑な法人構造、コルレス銀行関係、高額取引なども、EDDが必要となる場面です。FATF勧告はリスクに応じた措置の適用を求めています。",
        "tags": ["edd", "pep", "rba"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-013",
        "question": "USA PATRIOT Act §311に基づく「特別措置」（Special Measures）の内容として正しいものはどれか。",
        "questionEn": "What does USA PATRIOT Act §311 authorize as 'Special Measures'?",
        "options": [
            "A. 疑わしい取引報告（SAR）の免除",
            "B. 国内銀行の合併の承認",
            "C. 外国為替取引の全面禁止",
            "D. 主要なマネー・ローンダリング懸念先に対する特別措置（記録保持強化、コルレス関係の禁止等）"
        ],
        "answer": 3,
        "explanation": "USA PATRIOT Act §311は、FinCENが「主要なマネー・ローンダリング懸念先」（Primary Money Laundering Concern）として指定した外国の法域・金融機関・取引類型に対し、段階的な特別措置を課す権限を規定しています。措置には記録保持の強化、特定情報の報告、コルレス関係の制限・禁止等が含まれます。",
        "tags": ["us-law"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-014",
        "question": "ウォルフスバーグ・プライベートバンキング原則に基づき、EDD（強化された顧客管理）が必要なシナリオとして最も適切なものはどれか。",
        "questionEn": "Under the Wolfsberg Private Banking Principles, which scenario most clearly requires EDD?",
        "options": [
            "A. 国内の給与所得者が定期預金を開設する場合",
            "B. 中小企業が事業用口座を開設する場合",
            "C. 高リスク国出身の富裕層がプライベートバンキングを利用する場合",
            "D. 退職者が年金口座を開設する場合"
        ],
        "answer": 2,
        "explanation": "ウォルフスバーグ・プライベートバンキング原則に基づき、高リスク国出身の富裕層（wealthy individual from a high-risk country）がプライベートバンキングサービスを利用する場合は、EDDが必要です。資金源（SoF）、資産源（SoW）の詳細な確認、上級管理職の承認が求められます。",
        "tags": ["edd", "pep"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-015",
        "question": "FATF勧告10に基づくCDD措置に含まれるものとして最も適切なものはどれか。",
        "questionEn": "Which is the most appropriate CDD measure under FATF Recommendation 10?",
        "options": [
            "A. 口座開設時の一度きりの本人確認",
            "B. 取引関係の継続的な監視（Continuous Monitoring of Business Relationships）",
            "C. 顧客の政治的見解の確認",
            "D. 顧客の家族構成の詳細な調査"
        ],
        "answer": 1,
        "explanation": "FATF勧告10は、CDDの主要措置として、取引関係の継続的な監視（ongoing due diligence / continuous monitoring of the business relationship）を含んでいます。これは、取引パターンが顧客のリスクプロファイルと整合しているかを継続的に確認することを求めています。",
        "tags": ["cdd", "fatf", "monitoring"],
        "relatedJpQuestions": []
    },
    # ---- Deck 14 (Q66-Q70) ----
    {
        "id": "cams-d3-016",
        "question": "PEPが公職を退いた後の顧客管理義務として最も適切なものはどれか。",
        "questionEn": "What is the most appropriate obligation regarding a PEP who has left public office?",
        "options": [
            "A. 退任と同時にPEPとしての管理を即座に終了する",
            "B. 退任後は通常のCDDのみを適用する",
            "C. リスクベースで評価し、「一度PEPは常にPEP」の原則に基づき検討する",
            "D. 退任後5年間はすべての取引を禁止する"
        ],
        "answer": 2,
        "explanation": "PEPが公職を退いた後も、リスクベースで継続的な評価が必要です。「一度PEPは常にPEP」（Once a PEP, always a PEP）の原則に基づき、退任後も影響力が残存する可能性を考慮し、リスクに応じた期間（通常12～18ヶ月以上）EDDを継続すべきです。",
        "tags": ["pep", "rba"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-017",
        "question": "制裁スクリーニングの対象範囲として最も適切なものはどれか。",
        "questionEn": "What is the most appropriate scope for sanctions screening?",
        "options": [
            "A. 口座名義人のみをスクリーニングする",
            "B. すべての当事者およびField 70を含むすべてのフィールドをスクリーニングする",
            "C. 送金人と受取人のみをスクリーニングする",
            "D. $10,000超の取引のみをスクリーニングする"
        ],
        "answer": 1,
        "explanation": "制裁スクリーニングは、送金人、受取人、仲介銀行だけでなく、すべての当事者（all parties）およびSWIFTメッセージのField 70（支払い詳細情報）を含むすべてのフィールドをスクリーニングする必要があります。金額の閾値はなく、すべての取引が対象です。",
        "tags": ["sanctions", "filtering"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-018",
        "question": "EDD（強化された顧客管理）において、資金源（SoF）の確認はあるが、資産源（SoW）の確認が不十分な場合、何が欠如しているか。",
        "questionEn": "In an EDD context, if Source of Funds (SoF) has been verified but Source of Wealth (SoW) is lacking, what is deficient?",
        "options": [
            "A. SoF（資金源）の確認はあるが、SoW（資産源）の確認が欠如している",
            "B. SoW（資産源）の確認はあるが、SoF（資金源）の確認が欠如している",
            "C. CDDの全体が欠如している",
            "D. 取引モニタリングが欠如している"
        ],
        "answer": 0,
        "explanation": "SoF（Source of Funds）は個別の取引の資金源（例：特定の口座からの送金）を確認するものであり、SoW（Source of Wealth）は顧客の全体的な資産の出所（例：事業収入、相続、投資収益等）を確認するものです。EDDでは両方の確認が必要であり、SoFだけではSoWの欠如を補完できません。",
        "tags": ["edd", "cdd"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-019",
        "question": "取引モニタリング（TM）の閾値チューニングに関するガバナンスとして最も適切なものはどれか。",
        "questionEn": "What is the most appropriate governance approach for transaction monitoring threshold tuning?",
        "options": [
            "A. コンプライアンス部門の判断のみで閾値を変更する",
            "B. 営業部門の要望に基づいて閾値を引き上げる",
            "C. データ分析に基づき、モデルリスク管理（MRM）フレームワークの下でガバナンス承認を得る",
            "D. 閾値は導入時に固定し、変更しない"
        ],
        "answer": 2,
        "explanation": "取引モニタリングの閾値チューニングは、データ分析に基づく（data-driven analysis）客観的な根拠が必要であり、モデルリスク管理（Model Risk Management: MRM）フレームワークの下で、適切なガバナンス承認（governance approval）を得て実施すべきです。恣意的な変更は規制リスクを高めます。",
        "tags": ["monitoring", "governance", "it-system"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d3-020",
        "question": "SAR（疑わしい取引報告）の提出に関する規則として正しいものはどれか。",
        "questionEn": "Which statement correctly describes SAR filing rules?",
        "options": [
            "A. SARは90日以内に提出し、$1,000以上の疑わしい取引が対象",
            "B. SARは60日以内に提出し、顧客への通知が義務付けられている",
            "C. SARは提出後に顧客の同意を得る必要がある",
            "D. SARは30日以内（最大60日延長可能）に提出し、$5,000以上の取引が対象、ティッピングオフは禁止"
        ],
        "answer": 3,
        "explanation": "米国のSAR規則では、疑わしい活動を発見してから30日以内（被疑者の特定に時間を要する場合は最大60日）にSARを提出する必要があります。閾値は$5,000以上であり、SAR提出の事実を顧客に通知すること（tipping off）は禁止されています。",
        "tags": ["sar", "us-law"],
        "relatedJpQuestions": []
    },
]

# ---------------------------------------------------------------------------
# Domain 4: Investigation Process  (Q71-Q80)
# ---------------------------------------------------------------------------
domain4_questions = [
    # ---- Deck 15 (Q71-Q75) ----
    {
        "id": "cams-d4-001",
        "question": "不十分な監査証跡（Audit Trail）がもたらす最大のリスクは何か。",
        "questionEn": "What is the primary risk of poor audit trails?",
        "options": [
            "A. システムのパフォーマンス低下",
            "B. 規制当局への報告遅延",
            "C. 事象の再構築が困難になること",
            "D. 従業員の業務効率の低下"
        ],
        "answer": 2,
        "explanation": "不十分な監査証跡の最大のリスクは、疑わしい活動や取引の流れに関する事象の再構築（reconstruction of events）が困難になることです。調査や法執行への対応において、取引の時系列や意思決定プロセスを追跡できないことは、重大な障害となります。",
        "tags": ["investigation", "audit"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-002",
        "question": "FIU（金融情報機関）の主な機能として正しいものはどれか。",
        "questionEn": "What is the primary function of a Financial Intelligence Unit (FIU)?",
        "options": [
            "A. STR（疑わしい取引報告）を受理・分析・配信すること",
            "B. 金融機関を直接監督・検査すること",
            "C. 犯罪者の逮捕・起訴を行うこと",
            "D. 金融機関のAMLプログラムを設計すること"
        ],
        "answer": 0,
        "explanation": "FIU（Financial Intelligence Unit）の主な機能は、金融機関等から疑わしい取引報告（STR/SAR）を受理（receive）し、分析（analyze）し、法執行機関等に配信（disseminate）することです。FIUは監督機関でも捜査機関でもなく、金融情報のハブとして機能します。",
        "tags": ["investigation", "sar"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-003",
        "question": "「AMLの内部調査において、対象者を欺くことは適切な調査手法である」という記述は正しいか。",
        "questionEn": "Is the statement 'Deceiving the subject is an acceptable technique in an internal AML investigation' correct?",
        "options": [
            "A. 正しい。調査の効率性のために必要である",
            "B. 誤り。非倫理的であり、適切な調査手法ではない",
            "C. 場合による。上級管理職の承認があれば許容される",
            "D. 正しい。法執行機関との合同調査の場合に限り許容される"
        ],
        "answer": 1,
        "explanation": "AMLの内部調査において対象者を欺く（deceive）ことは、非倫理的（unethical）であり適切な調査手法ではありません。内部調査は客観的・公正に行われるべきであり、対象者の権利を尊重しつつ、事実を正確に把握することが求められます。欺瞞的手法は法的リスクも伴います。",
        "tags": ["investigation"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-004",
        "question": "法執行機関から「Keep Open Letter」（口座維持要請）を受け取った場合の最も適切な対応はどれか。",
        "questionEn": "What is the most appropriate response when receiving a 'Keep Open Letter' from law enforcement?",
        "options": [
            "A. 口座を直ちに閉鎖する",
            "B. 顧客にKeep Open Letterの存在を通知する",
            "C. 口座のすべての取引を停止する",
            "D. 口座を維持し、取引を監視し、必要に応じてSARを提出する"
        ],
        "answer": 3,
        "explanation": "Keep Open Letterは、法執行機関が捜査のために口座を開設状態で維持することを金融機関に要請する文書です。金融機関は口座を維持（keep open）し、取引を監視（monitor）し、疑わしい活動があればSARを提出する義務があります。顧客への通知はティッピングオフに該当するため禁止されます。",
        "tags": ["investigation", "le-response"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-005",
        "question": "サブピーナ（Subpoena）を発行できる機関として正しいものはどれか。",
        "questionEn": "Which entities can issue a subpoena?",
        "options": [
            "A. 金融機関のコンプライアンス部門",
            "B. FIU（金融情報機関）",
            "C. 大陪審（Grand Jury）、裁判所、またはDOJを通じた法執行機関",
            "D. 規制当局の検査官"
        ],
        "answer": 2,
        "explanation": "サブピーナ（召喚状・文書提出命令）は、大陪審（Grand Jury）、裁判所（Court）、またはDOJ（司法省）を通じた法執行機関（LEA）が発行できます。金融機関やFIUにはサブピーナの発行権限はありません。サブピーナには証言の求め（ad testificandum）と文書提出の求め（duces tecum）があります。",
        "tags": ["investigation", "le-response", "us-law"],
        "relatedJpQuestions": []
    },
    # ---- Deck 16 (Q76-Q80) ----
    {
        "id": "cams-d4-006",
        "question": "法執行機関から口頭で顧客記録の提供を求められた場合、最も適切な対応はどれか。",
        "questionEn": "What is the most appropriate response when law enforcement verbally requests customer records?",
        "options": [
            "A. 法執行機関の要請であるため直ちに提供する",
            "B. 有効な法的手続き（サブピーナ等）が提示されるまで拒否する",
            "C. 顧客の同意を得てから提供する",
            "D. 口頭の要請内容を記録し、後日メールで送付する"
        ],
        "answer": 1,
        "explanation": "法執行機関からの口頭の要請だけでは顧客記録を提供すべきではありません。有効な法的手続き（valid legal process）、すなわちサブピーナ、裁判所命令、捜索令状等が提示されるまで拒否するのが適切です。顧客情報の保護義務を果たしつつ、法的根拠に基づく正式な要請にのみ対応します。",
        "tags": ["le-response", "investigation"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-007",
        "question": "31 USC §5318(k)に基づく外国コルレス銀行への文書提出要求について、正しい記述はどれか。",
        "questionEn": "What correctly describes a records request to a foreign correspondent bank under 31 USC §5318(k)?",
        "options": [
            "A. 外国銀行にはこの要求に応じる法的義務はない",
            "B. 記録は外国銀行から直接入手でき、米国の仲介は不要である",
            "C. 記録を要求し、遵守がない場合はコルレス関係を終了する可能性がある",
            "D. この規定は米国内の銀行にのみ適用される"
        ],
        "answer": 2,
        "explanation": "31 USC §5318(k)は、米国の金融機関が外国コルレス銀行に対して記録の提出を要求できることを規定しています。外国銀行がこの要求に120時間以内に応じない場合、米国の金融機関はコルレス関係を終了（terminate）する義務を負う可能性があります。",
        "tags": ["us-law", "correspondent", "le-response"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-008",
        "question": "国家安全保障書簡（NSL: National Security Letter）を受け取った場合の金融機関の義務として正しいものはどれか。",
        "questionEn": "What is a financial institution's obligation upon receiving a National Security Letter (NSL)?",
        "options": [
            "A. 要求された記録を提出し、NSLの存在を開示してはならない",
            "B. NSLを公開し、顧客に通知する義務がある",
            "C. NSLの内容を規制当局に報告する",
            "D. NSLを拒否し、裁判所の命令を要求できる"
        ],
        "answer": 0,
        "explanation": "NSL（National Security Letter）を受け取った金融機関は、要求された記録を提出する義務があり、NSLの存在自体を開示してはなりません（nondisclosure requirement）。NSLはFBIなどの法執行機関が国家安全保障の調査に関連して発行する行政召喚状であり、裁判所の承認なく発行されます。",
        "tags": ["us-law", "le-response", "investigation"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-009",
        "question": "GDPR対象国の金融機関が外国の法執行機関からAML関連のデータ提供要請を受けた場合、最も適切な対応はどれか。",
        "questionEn": "When a financial institution subject to GDPR receives an AML data request from a foreign law enforcement agency, what is the most appropriate response?",
        "options": [
            "A. GDPRを理由にすべてのデータ提供を拒否する",
            "B. すべてのデータを無条件で提供する",
            "C. 一般的なデータは提供するが、STR情報はティッピングオフ禁止規定に基づき差し控える",
            "D. データ提供の可否について顧客に確認する"
        ],
        "answer": 2,
        "explanation": "GDPR対象国の金融機関は、正当な法的根拠に基づいて一般的な顧客データを提供できますが、STR（疑わしい取引報告）の情報はティッピングオフ禁止規定（tipping-off prohibition）に抵触するため差し控える必要があります。GDPRとAML規制のバランスを取ることが求められます。",
        "tags": ["privacy-law", "le-response", "sar"],
        "relatedJpQuestions": []
    },
    {
        "id": "cams-d4-010",
        "question": "国際的な情報共有に関する枠組みとして正しい組み合わせはどれか。",
        "questionEn": "Which combination correctly describes frameworks for cross-border information sharing?",
        "options": [
            "A. FATF勧告40のみが国際情報共有を規定している",
            "B. エグモント・グループのみがFIU間の情報交換を促進する",
            "C. 国際情報共有は各国の国内法にのみ依存し、国際的な枠組みは存在しない",
            "D. §314(b)（米国民間機関間共有）、FATF勧告18（金融グループ内共有）、APPI §28、PDPA §26などの複合的な枠組みが存在する"
        ],
        "answer": 3,
        "explanation": "国際的なAML/CFT情報共有は、複数の枠組みに基づいています。米国§314(b)は民間金融機関間の情報共有を許可し、FATF勧告18は金融グループ内の情報共有を求め、日本のAPPI（個人情報保護法）§28やシンガポールのPDPA §26は各国のデータ保護規制との整合性を規定しています。",
        "tags": ["international-cooperation", "privacy-law", "data-mgmt"],
        "relatedJpQuestions": []
    },
]

# ---------------------------------------------------------------------------
# Assemble the final JSON
# ---------------------------------------------------------------------------
cams_data = {
    "id": "cams",
    "name": "CAMS",
    "chapters": [
        {
            "id": "domain1",
            "name": "Domain 1: ML/TF Risks and Methods",
            "questions": domain1_questions,
        },
        {
            "id": "domain2",
            "name": "Domain 2: Compliance Standards",
            "questions": domain2_questions,
        },
        {
            "id": "domain3",
            "name": "Domain 3: AML/CFT Compliance Programme",
            "questions": domain3_questions,
        },
        {
            "id": "domain4",
            "name": "Domain 4: Investigation Process",
            "questions": domain4_questions,
        },
    ],
}

# Wrap in the same top-level structure used by questions.json
output = {"exams": [cams_data]}

# ---------------------------------------------------------------------------
# Write to file
# ---------------------------------------------------------------------------
out_path = "/home/user/aml-study-app/data/cams_questions.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
total = 0
for ch in cams_data["chapters"]:
    n = len(ch["questions"])
    total += n
    print(f"  {ch['id']} ({ch['name']}): {n} questions")

print(f"\nTotal questions: {total}")
assert total == 80, f"Expected 80 questions, got {total}"

# Verify answer indices are valid
for ch in cams_data["chapters"]:
    for q in ch["questions"]:
        assert 0 <= q["answer"] < len(q["options"]), (
            f"{q['id']}: answer index {q['answer']} out of range "
            f"(options count: {len(q['options'])})"
        )
        assert len(q["options"]) == 4, (
            f"{q['id']}: expected 4 options, got {len(q['options'])}"
        )

print("\nAll validations passed.")
print(f"Output written to {out_path}")
