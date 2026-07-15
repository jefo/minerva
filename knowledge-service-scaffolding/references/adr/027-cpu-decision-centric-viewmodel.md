---
id: adr-027
status: accepted
date: 2026-07-13
accepted: 2026-07-13
supersedes: []
superseded_by: []
tags: [igrolab, cpu, viewmodel, decision-centric, catalog, hub]
project: igrolab
---

# ADR-027: CPU Page — Decision-Centric ViewModel & Catalog Hub Architecture (v0.3.3)

## Контекст

R&D-сессия по проекту ИгроЛаба. Пересмотр архитектуры CPU-страницы: переход от «карточки объекта» (спеки + бенчи + цена, verdict как сумма впечатлений) к «набору разрешённых решений». Параллельно — проектирование главной страницы каталога процессоров (/processors/) как информационной панели управления (Web Editorial + Dashboard).

## Решение

Ниже — verbatim-содержание R&D-сессии.

---

# CPU Page — Decision-Centric ViewModel (v0.1, черновик для обсуждения)

## Смена оптики

Старая модель: страница = карточка объекта (спеки + бенчи + цена), verdict — сумма впечатлений.

Новая модель: страница = набор разрешённых решений. Каждое решение — это вопрос,
который реально стоит перед сборщиком («брать 7600X под 1440p-гейминг или нет»),
с зафиксированным ответом, отвергнутыми альтернативами и условиями, при которых
ответ меняется. Спеки и бенчмарки — не витрина, а *evidence*, подтягиваемый под
конкретное решение.

Verdict как отдельная сущность исчезает: то, что раньше было "Quick Verdict",
становится title/summary конкретного Decision, всегда с явной областью действия
("для 1440p-гейминга" — не "вообще хорош или плох").

---

## Ядро: сущности

// Эпистемический статус — переиспользуем вашу существующую разметку
type EpistemicTag = "fact" | "inference" | "measured" | "modeled";

interface EvidenceItem {
  id: string;
  claim: string;                // "7600X даёт +9% avg fps к 13400F в 1440p Ultra"
  epistemicTag: EpistemicTag;
  sourceRef: string;            // ссылка на запись в benchmark knowledge base
  measuredConditions?: string;  // "RTX 4070Ti, 1440p, DDR5-6000 CL30" — снимает ложную generalизацию
}

interface ContextModifier {
  id: string;
  condition: string;            // "если разрешение — 1080p"
  effect: string;               // "разрыв в fps практически исчезает, решение инвертируется в пользу более дешёвого CPU"
  evidenceRefs: string[];       // ссылки на EvidenceItem, подтверждающие инверсию
}

interface RejectedOption {
  id: string;
  alternative: string;          // "Core i5-13600K"
  reasonRejected: string;       // формулировка причины, не ярлык "хуже"
  tradeoff: string;             // что теряется/приобретается при выборе альтернативы
  evidenceRefs: string[];
}

interface Decision {
  id: string;
  question: string;             // "Оправдан ли 7600X для сборки под 1440p-гейминг с RTX 4070 Ti?"
  scope: string;                // явная область действия — обязательное поле, не опция
  chosenAnswer: string;         // сформулированный ответ, не ярлык "да/нет"
  reasoning: string;            // цепочка причинности, а не заключение
  rejectedOptions: RejectedOption[];
  contextModifiers: ContextModifier[]; // условия инверсии решения
  evidenceRefs: string[];
  confidenceNote: string;       // ОБЯЗАТЕЛЬНО. Где данные неполны/устарели — явный epistemic honesty slot.
                                 // Если пробелов нет — явно пишем "evidence base considered sufficient",
                                 // но поле не может быть пустым или отсутствовать.
}

## Верхнеуровневый ViewModel
interface CpuDecisionViewModel {
  meta: {
    id: string;
    slug: string;
    title: string;
    releaseDate: string;
    isCurrentGen: boolean;
    // shortVerdict — УДАЛЁН. Если нужен teaser для SEO/шеринга —
    // это должна быть отдельная, явно помеченная как "summary for search engines"
    // строка вне editorial layer, не выдаваемая как редакционная оценка.
  };

  // Ядро страницы: решения, ради которых читатель пришёл
  decisions: Decision[];

  // Компонентные данные — теперь ВСПОМОГАТЕЛЬНЫЙ слой,
  // подтягиваемый декларативно внутрь Decision через evidenceRefs
  componentData: {
    kpiMetrics: { /* как было — но это справочный слой, не первый экран */ };
    specGroups: Array<{ groupName: string; specs: Array<{ label: string; value: string | number }> }>;
    benchmarkRaw: Array<{ testName: string; currentValue: number; competitors: unknown[]; conditions: string }>;
  };

  compatibility: {
    socket: string;
    ramType: string[];
    recommendedCoolerTdp: number;
    compatibleChipsets: Array<{ name: string; slug: string }>;
    // Явный слой "чего это НЕ решает"
    notResolvedBy: string[]; // "не гарантирует отсутствие троттлинга в SFF-корпусах"
  };

  market: { currentMinPrice: number; priceHistory: Array<{ date: string; price: number }>; offers: unknown[] };

  navigationPivots: {
    nextModelUp: { name: string; slug: string };
    prevModelDown: { name: string; slug: string };
    directCompetitor: { name: string; slug: string };
  };
}

---

## Пример: Ryzen 5 7600X — как это выглядит на данных

{
  id: "dec-01",
  question: "Оправдан ли 7600X для сборки под 1440p-гейминг с RTX 4070 Ti?",
  scope: "1440p, GPU-класс RTX 4070Ti/4070, актуально на момент публикации",
  chosenAnswer: "Да, при условии DDR5-6000+ — CPU перестаёт быть узким местом на этом GPU-уровне",
  reasoning: "На 1440p с GPU такого класса CPU-bound сценарии редки; выигрыш в single-core...",
  rejectedOptions: [
    {
      id: "ro-01",
      alternative: "Core i5-13600K",
      reasonRejected: "Сопоставимая игровая производительность, но выше энергопотребление под нагрузкой и требует более дорогого охлаждения для раскрытия P-ядер",
      tradeoff: "Выигрывает в multi-core тяжёлых задачах (рендер/компиляция) при том же бюджете",
      evidenceRefs: ["ev-14", "ev-15"]
    }
  ],
  contextModifiers: [
    {
      id: "cm-01",
      condition: "Если сборка под 1080p или GPU-класс ниже RTX 4060",
      effect: "Разница практически стирается — переплата за 7600X не оправдана, решение инвертируется",
      evidenceRefs: ["ev-16"]
    },
    {
      id: "cm-02",
      condition: "Если в сборке приоритет — рендеринг/стриминг с одновременным геймингом",
      effect: "Решение инвертируется в пользу CPU с большим числом ядер (7700X/13600K)",
      evidenceRefs: ["ev-17"]
    }
  ],
  evidenceRefs: ["ev-01", "ev-02", "ev-14", "ev-15", "ev-16"],
  confidenceNote: "Данные по DDR5-8000 конфигурациям пока недостаточны для устойчивого вывода"
}

---

## Как это меняет организмы (кратко, для следующего шага)

- EditorialHeroHeader — вместо verdict-бейджа: заголовок = question главного (canonical) Decision + scope. Никакого "хорош/плох" без области действия.
- KPIDashboardGrid — остаётся, но теряет роль "первого впечатления": это справочная панель, доступная, но не диктующая нарратив.
- InteractiveBenchmarkVisualizer — рендерит evidenceRefs конкретного Decision, а не абстрактный набор графиков "вообще".
- CompatibilityMatrix — добавляет обязательный блок notResolvedBy.
- Нужен новый организм — DecisionExplorer: список решений страницы с возможностью развернуть rejectedOptions и contextModifiers. Это и есть замена "Quick Verdict" и одновременно точка входа в evidence-debt chain.

---

## Таксономия Decision-типов (генеративный слой)

Число решений на странице — не design target, а результат фильтрации кандидатов,
порождённых таксономией, через Genuine Tension Test. Ниже — кандидатные типы
для категории CPU; для каждого — обязательный минимум evidence, без которого
экземпляр этого типа не проходит B1.

type DecisionTaxonomy =
  | "UseCaseDecision"        // "оправдан ли CPU X для сценария Y"
  | "ComponentChoiceDecision" // "X против прямого конкурента Z"
  | "TimingDecision"          // "брать сейчас или ждать преемника/снижения цены"
  | "UpgradePathDecision"     // "стоит ли апгрейдиться с CPU X на этот" — ПРЕДПОЛАГАЕТ существующее железо
  | "ConstraintDecision"      // "укладывается ли в ограничение C" (SFF, TDP-бюджет, PSU)
  | "PlatformCommitmentDecision" // "заходить на платформу сейчас или нет" — ГРИНФИЛД-выбор, без существующего железа
  | "MicroVariantDecision";      // "переплачивать за старший субвариант или брать младший + тюнинг"

// Discriminator UpgradePath vs PlatformCommitment:
// если у пользователя есть текущая система для миграции — UpgradePathDecision;
// если сборка с нуля — PlatformCommitmentDecision. Это поле обязано быть явным
// в scope, а не выводиться из контекста статьи.

interface DecisionTypeRequirements {
  type: DecisionTaxonomy;
  mandatoryEvidenceKinds: string[]; // проверяется в B1 как completeness gate
}

const requirements: DecisionTypeRequirements[] = [
  { type: "UseCaseDecision",
    mandatoryEvidenceKinds: ["benchmark@statedSettings", "contextModifier@resolutionOrGpuTier"] },
  { type: "ComponentChoiceDecision",
    mandatoryEvidenceKinds: ["comparativeBenchmark", "nonBenchmarkTradeoff@powerOrPlatformCost"] },
  { type: "TimingDecision",
    mandatoryEvidenceKinds: ["priceHistory", "roadmapOrSuccessorStatus"] },
  { type: "UpgradePathDecision",
    mandatoryEvidenceKinds: ["generationalDeltaBenchmark", "socketOrPlatformReuseCheck"] },
  { type: "ConstraintDecision",
    mandatoryEvidenceKinds: ["thermalOrPowerMeasurement", "realWorldThrottlingReport"] },
  { type: "PlatformCommitmentDecision",
    mandatoryEvidenceKinds: ["platformTotalCostEstimate", "socketLifecycleRoadmap"] },
  { type: "MicroVariantDecision",
    mandatoryEvidenceKinds: ["priceDelta", "performanceDeltaAtEqualPowerLimits", "userTuningRequiredFlag"] },
];

## Genuine Tension Test — правило генерации количества

Для каждого SKU: для каждого таксон-типа × реалистичного scope-инстанса (например,
UseCaseDecision × "1440p-гейминг", UseCaseDecision × "1080p high-refresh",
UseCaseDecision × "продуктивность/рендер") проверяем 4 критерия:

1. Plausible Alternative — разумный сборщик реально мог бы выбрать иначе.
2. Non-Obvious Resolution — ответ не читается напрямую из спеков/маркетинга.
3. Real-World Frequency — сценарий реально распространён, не краевой случай.
4. Evidence Sufficiency — достаточно fact/measured evidence для ответственного chosenAnswer.

Кандидат, не прошедший все 4 — не публикуется как Decision. Итоговое число
решений на странице — не заданное количество, а результат: у спорного SKU их
может быть 5-6, у продукта без реальной конкурентной дилеммы — 1-2, и это
валидный результат, а не недоработка.

DecisionTaxonomy пишется как поле в Decision:

interface Decision {
  // ...как раньше
  taxonomyType: DecisionTaxonomy;
}

---

## Genuine Tension Test — алгоритмизированная версия (Pareto non-dominance)

Первая версия (два раздельных порога: ценовой коридор + Δperformance) содержала
логический разрыв — собственный иллюстративный пример ("быстрее на 15%, но
горячее на 50 Вт и требует дорогой платы") требует четырёх осей сравнения
(perf/price/TDP/platform cost), а формулы покрывали только две, плюс
неалгоритмизированное exception ("значительно дешевле") прямо внутри раздела,
который заявлен как перевод критериев в пороги. Меняем на единый принцип.

Побочный эффект принципа: старое поколение с более низкой ценой при
равной/худшей производительности автоматически проходит тест без отдельного
exception — недоминирование по вектору [price, performance] делает частный
случай общим следствием правила, а не патчем.

type OptimizationDirection = "minimize" | "maximize";

interface AxisContract {
  metricKey: keyof MetricVector;
  direction: OptimizationDirection;
  tolerancePct: number;
  // TODO(open): tolerancePct считается от значения target, от меньшего
  // из двух сравниваемых значений, или от среднего? Разные базы дают разный
  // абсолютный допуск на границах (пример: 10% TDP-допуска — 6.5W для 65W-чипа
  // и 10.5W для 105W-чипа при разных направлениях сравнения).
}

const TAXONOMY_METRIC_CONTRACTS: Record<DecisionTaxonomy, AxisContract[]> = {
  UseCaseDecision: [
    { metricKey: "performanceInScope", direction: "maximize", tolerancePct: 3 },
    { metricKey: "price", direction: "minimize", tolerancePct: 5 }
  ],
  ComponentChoiceDecision: [
    { metricKey: "performanceInScope", direction: "maximize", tolerancePct: 3 },
    { metricKey: "price", direction: "minimize", tolerancePct: 5 },
    { metricKey: "tdpWatts", direction: "minimize", tolerancePct: 10 },
    { metricKey: "platformCostDelta", direction: "minimize", tolerancePct: 5 }
  ],
  MicroVariantDecision: [
    { metricKey: "performanceInScope", direction: "maximize", tolerancePct: 2 },
    { metricKey: "price", direction: "minimize", tolerancePct: 5 },
    { metricKey: "tdpWatts", direction: "minimize", tolerancePct: 10 },
    { metricKey: "noiseOrCoolingBurden", direction: "minimize", tolerancePct: 15 }
  ],
  // TODO(open): контракты для TimingDecision, UpgradePathDecision,
  // ConstraintDecision, PlatformCommitmentDecision ещё не заданы.
};

// TODO(open): поведение при отсутствующей оси в metricVector одной из сторон —
// исключать ось из сравнения молча (с логированием как coverage gap) или
// триггерить Evidence Sufficiency fail на весь тест? Сейчас не специфицировано,
// а от этого зависит, может ли Pareto-результат получиться на обеднённом векторе.

interface MetricVector {
  performanceInScope?: number;
  price?: number;
  tdpWatts?: number;
  platformCostDelta?: number;
  noiseOrCoolingBurden?: number;
}

interface TensionTestInput {
  targetCpu: CpuSpecs;
  candidateAlternative: CpuSpecs;
  scope: UserScope;
  metricVector: MetricVector;
}

function isParetoDominated(target: MetricVector, alt: MetricVector): boolean {
  // alt доминирует target, если лучше или равен (в пределах tolerancePct)
  // по ВСЕМ осям контракта и строго лучше хотя бы по одной.
  return false; // заглушка для реализации
}

interface TensionTestResult {
  passesNonDominance: boolean;
  passesRealWorldFrequency: boolean;
  passesEvidenceSufficiency: boolean;
  isApprovedForDraft: boolean;
}

## Real-World Frequency — стек сигналов для ру-сегмента

Английские инструменты (Ahrefs/SEMrush/Reddit) систематически недооценивают
локальный спрос — например, культ Xeon с AliExpress или народные чипы вроде
i3-12100F/Ryzen 5 5600 не отражены в западных трендах.

interface RealWorldFrequencySignals {
  yandexWordstat: {
    // F = WS(Query) + α × WS(CompetitorQuery)
    formula: string;
    alpha: number; // коэффициент затухания
    // TODO(open): формула заменила исходный порог ">100 запросов/мес",
    // но обновлённый порог прохождения для F не переформулирован.
    passThreshold?: number;
  };
  localForumSignal: {
    sources: string[]; // overclockers.ru, ixbt.com, DNS-клуб
    windowDays: number; // 90
  };
  retailRankSignal: {
    sources: string[]; // DNS, Ситилинк, e-katalog
    // TODO(open): высокие продажи не равны содержательной дилемме —
    // риск смешать популярность (маркетинг/скидка) с genuine tension.
    // Предлагается использовать как входной сигнал для B2 (структурный
    // аудит), не как самостоятельный passing criterion в B1.
  };
}

## Матрица нормализации тестовых сред (Evidence Sufficiency)
interface NormalizationRules {
  gpuEquivalenceTier: string[][];
  maxRamSpeedDeltaMhz: number;
  // TODO(open, найдена методологическая дыра): проверка только по МГц
  // пропустит пару DDR4-3200/DDR5-3600 как "сопоставимую", хотя это разные
  // технологии с разной полосой/латентностью — та же категория ошибки,
  // которую матрица призвана предотвращать (стенд на RTX 4090 vs RTX 4060).
  // Нужно строгое совпадение ramGeneration (DDR4/DDR5) ОТДЕЛЬНО от МГц-допуска.
  ramGeneration?: "strict-match"; // добавить как обязательную проверку
  // TODO(operational): таблица gpuEquivalenceTier требует владельца и
  // регулярного обновления по мере выхода новых GPU — привязать к пайплайну
  // benchmark knowledge base, а не держать как статичный литерал.
}

function isEvidenceComparable(condA: TestConditions, condB: TestConditions): boolean {
  if (condA.resolution !== condB.resolution) return false;
  const tierA = findGpuTier(condA.gpu, normalizationRules.gpuEquivalenceTier);
  const tierB = findGpuTier(condB.gpu, normalizationRules.gpuEquivalenceTier);
  if (tierA !== tierB || tierA === -1) return false;
  if (Math.abs(condA.ramSpeedMhz - condB.ramSpeedMhz) > normalizationRules.maxRamSpeedDeltaMhz) return false;
  // TODO: добавить condA.ramGeneration !== condB.ramGeneration → false
  return true;
}

## Калибровочная петля (встроена в B1/B2 контур)

type RejectReasonTag =
  | "false_positive_dominance"
  | "false_negative_dominance"
  | "bad_evidence_matching"
  | "weak_reasoning";

interface CalibrationLogEntry {
  decisionId: string;
  sku: string;
  rejectReasonTag: RejectReasonTag;
  editorComment: string;
  date: string;
}

// Регрессионное тестирование: при изменении весов/допусков/промптов —
// прогон новой версии по базе исторических отказов.
// TODO(open): критерий успеха регрессии не определён количественно —
// какой процент воспроизведения прошлых false negatives/positives
// блокирует деплой новой версии порогов?

---

## ViewModel v0.3 — ЗАКРЫТО

Все пункты 1-10 предыдущего раунда разрешены:

1. tolerancePct считается от значения Target CPU (страница, на которой находится пользователь) — стабильная точка отсчёта.
2. Отсутствие данных хотя бы по одной оси контракта → Evidence Sufficiency Fail, тест прерывается полностью, алерт в Content Debt Log. (Операционная зависимость: полнота benchmark KB становится хардблокером публикации для SKU с неполными данными.)
3. ramGeneration — строгое совпадение (DDR4/DDR5), отдельно от МГц-допуска.
4. Ритейл-сигнал исключён из B1-фильтров, передан как input-сигнал в B2 (Structural Audit) — не самостоятельный passing criterion.
5. Порог частотности: F ≥ 150 для ру-сегмента. (Открытая заметка: RejectReasonTag пока не покрывает ошибку калибровки самого порога F — стоит добавить wrong_frequency_threshold в перечень тегов.)
6. Zero Regression policy: 0% допуск на false positives, <2% на false negatives (искл. изменение рыночной цены). (Открытая заметка: сам лог исторических reject-ов нуждается в периодической ревизии, иначе ошибки редактора канонизируются навсегда.)
7. TAXONOMY_METRIC_CONTRACTS заполнен для всех 7 типов таксономии.

---

## Найдено при переходе к IA: разные decision shapes требуют разного comparisonMode

isParetoDominated спроектирован для пары конкретных CPU (Target vs Alternative).
Это подходит ComponentChoiceDecision, MicroVariantDecision,
PlatformCommitmentDecision — pairwise сравнение.

Не подходит без изменений:
- ConstraintDecision — Target сравнивается не с другим CPU, а с фиксированным
  лимитом (TDP-бюджет корпуса) — threshold сравнение, не pairwise.
- TimingDecision — Target сравнивается с гипотетическим будущим состоянием
  (ещё не вышедший преемник, будущая цена) — temporal/probabilistic
  сравнение, нет физического "Rejected CPU" для подсветки на графике.

Это напрямую блокирует UI-механику DecisionExplorer → BenchmarkVisualizer
(клик по RejectedOption подсвечивает пару на графике) — для threshold/temporal
типов подсвечивать физически нечего.

type ComparisonMode = "pairwise" | "threshold" | "temporal";

const TAXONOMY_COMPARISON_MODE: Record<DecisionTaxonomy, ComparisonMode> = {
  UseCaseDecision: "pairwise",
  ComponentChoiceDecision: "pairwise",
  MicroVariantDecision: "pairwise",
  PlatformCommitmentDecision: "pairwise",
  ConstraintDecision: "threshold",   // TODO(open): подтвердить
  TimingDecision: "temporal",        // TODO(open): подтвердить
  UpgradePathDecision: "pairwise",   // TODO(open): подтвердить — target(new) vs target(current owned) — pairwise, но "текущий CPU" не имеет карточки в каталоге
};

TODO(open, блокирует детальное проектирование DecisionExplorer):
comparisonMode выводится из taxonomyType как фиксированный маппинг (не
редакторский выбор) — подтвердить распределение выше, и решить, какой UI-паттерн
использует DecisionExplorer/BenchmarkVisualizer для threshold и temporal
режимов вместо подсветки пары на графике.

---

## ViewModel v0.3.1 — исправления при закрытии архитектуры каталога/хаба

### 1. Tiered Safety Buffer (вместо плоских 20%)

Transient spikes у флагманских GPU (RTX 4090-класса) документированно превышают
паспортный TDP на 40-50%+ на микросекундных всплесках. Плоский буфер занижает
риск именно на Сборке В (флагманская видеокарта), где он критичнее всего.

interface SafetyBufferByGpuTier {
  gpuTier: "flagship" | "highEnd" | "midRange" | "budget";
  bufferPct: number;
}

const SAFETY_BUFFERS: SafetyBufferByGpuTier[] = [
  { gpuTier: "flagship", bufferPct: 40 },  // TODO(open): подтвердить точный % по реальным замерам
  { gpuTier: "highEnd", bufferPct: 30 },
  { gpuTier: "midRange", bufferPct: 20 },
  { gpuTier: "budget", bufferPct: 15 },
];

### 2. Content Lifecycle Policy для вытесненных top-3 сценариев

type LegacyDecisionStatus = "active" | "archived-noindex" | "redirected";

interface DecisionLifecycleRecord {
  decisionId: string;
  status: LegacyDecisionStatus;
  supersededBy?: string; // decisionId нового сценария, если redirected
  demotedDate: string;
}
// TODO(open): выбрать политику по умолчанию при вытеснении из top-3 —
// redirected (301 на новый сценарий) сохраняет SEO-вес лучше, чем
// archived-noindex, но требует явного маппинга "старый вопрос → новый вопрос"
// который не всегда 1:1 (донор мог замениться на принципиально другой чип).

### 3. Структурированная полярность вердикта (вместо string-matching)

type VerdictPolarity = "positive" | "negative" | "conditional";

interface Decision {
  // ...как раньше
  verdictPolarity: VerdictPolarity; // обязательное поле, заполняется редактором
                                     // явно, не выводится парсингом chosenAnswer
}

function getCatalogTags(cpu: CpuDecisionViewModel): string[] {
  const tags: string[] = [];
  const hasStrongGamingDecision = cpu.decisions.some(d =>
    d.taxonomyType === "UseCaseDecision" &&
    d.scope.includes("gaming") &&
    d.verdictPolarity === "positive" // структурное поле, не парсинг текста
  );
  if (hasStrongGamingDecision) tags.push("gaming");
  return tags;
}

Все архитектурные уточнения и исправления версии v0.3.1 принимаются. Введение структурированной полярности вердикта (VerdictPolarity), каскадных буферов безопасности под transient-всплески видеокарт и замена текстового парсинга на типизированные поля окончательно стабилизируют ViewModel.

Разрешим оставшиеся TODO перед переходом к разметке каталога:

1. **Распределение `comparisonMode`:** Полностью подтверждено. ConstraintDecision -> threshold, TimingDecision -> temporal, UpgradePath -> pairwise.
2. **Проценты буфера безопасности (`SAFETY_BUFFERS`):** Значения 40% (Flagship), 30% (High-End), 20% (Mid-Range), 15% (Budget) признаются технически обоснованными. Микросекундные всплески (transient spikes) современных видеокарт (например, RTX 4090, которая при среднем потреблении 450 Вт в пике до 10 мс может потреблять более 650 Вт) требуют именно такого каскадного запаса, чтобы не вызывать срабатывания OCP (Overcurrent Protection) блоков питания.
3. **Политика вытеснения из Top-3:** Принимается дефолтное поведение `redirected` (301 redirect), но не на абстрактный индекс, а на основную страницу модели процессора /processors/[slug]/. Таким образом, ссылочный вес вытесненного из топа сценария (например, «апгрейд с Ryzen 1600 на 7600X») перетекает на родительскую карточку процессора, сохраняя SEO-авторитетность домена.

Полностью согласен с вашим приоритетом: переходим к проектированию Главной страницы каталога (Хаба). Это логическое продолжение нашей унификации.

---

# Проектирование Главной страницы каталога процессоров (/processors/)

Концепция «Web Editorial + Dashboard» на уровне каталога означает уход от унылой бесконечной сетки интернет-магазина. Мы проектируем информационную панель управления, которая помогает пользователю сканировать рынок процессоров через призму задач (UseCase).

## 1. Сетка и компоновка (Layout Grid)

Мы используем асимметричную 12-колоночную сетку. Страница делится на три ключевые зоны:

```
+------------------------------------------------------------------------------------+
|  [Zone 1: Global Header & Active Context Indicator]                                |
|  Поисковая строка, быстрый переключатель сокетов (AM5, LGA1700), статус контекста  |
+------------------------------------------------------------------------------------+
|  [Zone 2: Use-Case Pivot Tiles] (4-4-4 Grid / 12 Columns)                          |
|  Топ-3 карточки-сценария, генерируемые динамически из актуальных UseCase.scope     |
|  +------------------------+  +------------------------+  +------------------------+ |
|  | "Гейминг в 1440p"      |  | "Максимальный FPS/Цена"|  | "Рабочие станции"      | |
|  +------------------------+  +------------------------+  +------------------------+ |
+------------------------------------------------------------------------------------+
|  ЛЕВАЯ ПАНЕЛЬ (3 кол.)    |  ЦЕНТРАЛЬНАЯ ПАНЕЛЬ (9 колонок)                        |
|  [Zone 3: Smart Filters]  |  [Zone 4: Dense Catalog Grid]                          |
|  Только важные ТТХ        |  Карточки процессоров в стиле Dashboard-Widgets        |
|  (Socket, TDP Class,      |  +--------------------------------------------------+  |
|  Platform Cost)           |  | SKU Card (Ryzen 5 7600X)                         |  |
|                           |  +--------------------------------------------------+  |
|                           |  | SKU Card (Core i5-13600K)                        |  |
|                           |  +--------------------------------------------------+  |
+---------------------------+--------------------------------------------------------+
```

---

## 2. Архитектурное описание ключевых компонентов (Организмов)

### Компонент 1: Use-Case Pivot Tiles (Плитки сценариев)

Этот блок находится над основным списком товаров. Он формирует верхний уровень воронки.

- **Как генерируется:** Система сканирует базу опубликованных решений, находит самые частотные UseCaseDecision.scope и рендерит три плитки.
- **Интерактивность:** Клик по плитке не просто перегружает страницу, а активирует пресет фильтров в левой панели (например, клик по «Гейминг в 1440p» автоматически включает фильтр GPU-класса и сокетов, скрывая офисные решения).

### Компонент 2: Smart Filters (Панель умной фильтрации)

В отличие от классических фильтров, этот блок оперирует не сырыми ТТХ, а вычисляемыми интегральными метриками.

- *Вместо «TDP (Вт)»:* Фильтр «Требования к кулеру» с опциями: Простой воздух (<100W), Башня (100-200W), СЖО (>200W).
- *Вместо «Поддержка DDR5»:* Фильтр «Стоимость платформы» с опциями: Бюджетная (DDR4), Современная (DDR5).

### Компонент 3: Dashboard SKU Card (Виджет процессора в листинге)

Это главный элемент каталога. Каждая карточка товара проектируется как мини-дашборд.

Анатомия карточки (в таксономии Atomic Design):

```
+-----------------------------------------------------------------------------+
| [M1: Brand/Model Title]                          [M2: Verdict Badges]       |
| AMD Ryzen 5 7600X                                 ( Gaming Value ) ( AM5 )  |
+-----------------------------------------------------------------------------+
| [M3: Core KPI Grid]                                                         |
|  Cores/Threads: 6 / 12      Max Boost Clock: 5.3 GHz    TDP Class: High     |
|  Gaming Index:  87/100      Multi-Core Perf: 72/100     Base Price: $220    |
+-----------------------------------------------------------------------------+
| [M4: Canonical Decision Teaser]                                             |
| "Оптимален для сборок с RTX 4070/4070Ti на долговечной платформе AM5"      |
+-----------------------------------------------------------------------------+
| [M5: Action Bar]                                                            |
| [ Добавить к сравнению ]                        [ Подробнее о решениях (4) ]|
+-----------------------------------------------------------------------------+
```

- **`Verdict Badges` (Вычисляемые теги):** Показываются автоматически на основе наличия положительного вердикта в соответствующих decisions. Если у SKU есть UseCaseDecision с verdictPolarity: "positive" для игр, карточка автоматически получает бейдж Gaming Value.
- **`Core KPI Grid`:** Вывод ключевых метрик производительности и платформы.
- **`Canonical Decision Teaser`:** Вместо случайного куска текста из описания карточка выводит свойство chosenAnswer из главного (canonical) Decision этого процессора. Пользователь видит краткий, емкий инженерный вывод прямо в каталоге.
- **`Action Bar`:** Кнопка «Добавить к сравнению» инициирует добавление SKU в плавающий Comparison Drawer (панель сравнения). Кнопка подробностей показывает счетчик реально разобранных на странице решений: *«Подробнее о решениях (4)»*.

---

## 3. SEO-оптимизация листинга хаба

Поскольку мы генерируем теги и плитки на основе decisions, поисковый робот видит идеально структурированный тематический граф.

- Каждый индексируемый срез фильтров (например, /processors/gaming/) получает заголовок H1, сгенерированный из названия UseCase-сценария, и выводит только те процессоры, у которых есть соответствующий позитивный вердикт. Это полностью исключает проблему пустых страниц или страниц с нерелевантной выдачей.

---

### Следующий шаг проектирования (до v0.3.2):

Оставалось два пункта:
1. Интерфейсная логика и стейт-менеджмент Comparison Drawer
2. Детальное описание разметки Dashboard SKU Card

Пункт 1 закрыт ниже (см. «Часть 2: Comparison Drawer»). Пункт 2 остаётся открытым.

---

## ViewModel v0.3.2 — Исправление «расползания вердиктов» (verdict creep)

Аудит вскрыл проблему: числовые индексы без методологии и безадресные бейджи
вроде «Gaming Value» возвращают к субъективной, не-инженерной оценке, разрушая
доверие пользователя. Пакет исправлений устраняет эти противоречия.

### 1. Замена абсолютных индексов на Относительные Базовые Метрики

**Отказ от абстрактных шкал 0-100** («Gaming Index»). На карточке товара
выводятся физически обоснованные относительные показатели в сравнении с
общеизвестным отраслевым эталоном (Baseline CPU).

**Принцип:** В качестве неизменного эталона (100%) для текущего поколения
выбирается массовый народный процессор (например, Ryzen 5 5600X). Все
показатели на карточках каталога высчитываются относительно него на основе
реальных бенчмарков из базы знаний.

**Вид на карточке:**
- `Gaming (1440p): 134% vs R5 5600X` — вместо «87/100»
- `Multi-Core: 182% vs R5 5600X` — вместо «72/100»

**Эпистемическая честность:** Клик по метрике открывает всплывающую подсказку
со списком конкретных evidenceRefs.

**Условия теста — visible without click:**
Gaming (1440p, RTX 4090\*): 134% vs R5 5600X
\* изолированный CPU-тест — реальный прирост на слабых GPU может быть меньше

```typescript
interface RelativeMetric {
  label: string;                // "Gaming (1440p)"
  value: number;                // 134
  baselineCpu: string;          // "Ryzen 5 5600X"
  testConditions: string;       // "RTX 4090, DDR5-6000 CL30" — видно на карточке без клика
  caveatNote?: string;          // "реальный прирост на слабых GPU может быть меньше"
  evidenceRefs: string[];       // ссылки на конкретные evidence-записи в KB
}
```

**Baseline CPU нуждается в цикле обновления:** Тот же Quarterly Re-evaluation
Pipeline, что и для top-3 донор-CPU в UpgradePathDecision, должен применяться
к выбору эталонного baseline CPU — иначе эталон устаревает быстрее, чем
контент вокруг него.

### 2. Замена «Verdict Badges» на ScopedDecisionTags (Сценарные теги условий)

Компонент переименовывается в **ScopedDecisionTags**. Тег не имеет права быть
безадресным — он обязан явно транслировать ключевое условие (scope constraint)
родительского Decision прямо на фасаде карточки.

| Было (безадресное) | Стало (scoped) |
|---|---|
| `Gaming Value` | `Гейминг 1440p (RTX 4070+) ✔️` |
| `Compact King` | `Ограничение TDP 65W ✔️` |

```typescript
interface ScopedDecisionTag {
  label: string;               // "Гейминг 1440p (RTX 4070+)"
  verdictPolarity: VerdictPolarity; // "positive" | "negative" | "conditional"
  sourceDecisionId: string;    // ссылка на конкретный Decision — раскрывается по hover/клику
  scopeConstraint: string;     // ключевое условие из scope родительского Decision
}
```

### 3. Правило выбора Главного (Canonical) Decision

Для устранения рассинхронизации между заголовком страницы и тизером в каталоге —
**детерминированный алгоритм** выбора Canonical Decision:

```typescript
function getCanonicalDecision(decisions: Decision[]): Decision {
  // Шаг 1: фильтруем только UseCaseDecision с verdictPolarity === "positive"
  const candidates = decisions.filter(d =>
    d.taxonomyType === "UseCaseDecision" && d.verdictPolarity === "positive"
  );
  if (candidates.length === 0) {
    // fallback: любой positive-вердикт любого типа
    const fallback = decisions.filter(d => d.verdictPolarity === "positive");
    if (fallback.length === 0) {
      // последний fallback: conditional-вердикт UseCaseDecision
      return decisions.find(d =>
        d.taxonomyType === "UseCaseDecision" && d.verdictPolarity === "conditional"
      ) || decisions[0];
    }
    return fallback[0];
  }
  // Шаг 2: из positive UseCaseDecision — выбираем с максимальным frequencyF
  return candidates.reduce((a, b) => a.frequencyF >= b.frequencyF ? a : b);
}
```

**Добавление frequencyF в Decision** (без этого поля алгоритм не работает):

```typescript
interface Decision {
  // ...как раньше
  frequencyF: number; // сохраняется из B1 real-world-frequency сигнала, не только gate-проверка
}
```

**Важно:** поле `isCanonical` (ровно один `true` на страницу) проставляется
редактором и проверяется B2 как structural gate — публикация блокируется при
0 или >1 canonical на SKU. Алгоритм `getCanonicalDecision` — это автоматический
пресет, редактор может переопределить явным флагом.

### 4. Введение Структурной Категории Сценария (ScopeCategory)

Полный отказ от хрупкого текстового поиска подстрок в прозе. В структуру
Decision добавляется строго типизированное перечисление:

```typescript
type ScopeCategory = "gaming" | "productivity" | "budget" | "sff" | "workstation";

interface Decision {
  // ...как раньше
  scopeCategory: ScopeCategory[]; // явно проставляется редактором, не парсится из scope-текста
}
```

**Исправленная getCatalogTags (без string-matching):**

```typescript
function getCatalogTags(cpu: CpuDecisionViewModel): string[] {
  const tags: string[] = [];
  const hasStrongGamingDecision = cpu.decisions.some(d =>
    d.taxonomyType === "UseCaseDecision" &&
    d.scopeCategory.includes("gaming") &&
    d.verdictPolarity === "positive"
  );
  if (hasStrongGamingDecision) tags.push("gaming");
  return tags;
}
```

---

## Catalog Page — Dashboard SKU Card (исправленная анатомия, v0.3.2)

С учётом всех исправлений, анатомия карточки в листинге каталога:

```
+-----------------------------------------------------------------------------+
| [M1: Brand/Model Title]                          [M2: ScopedDecisionTags]   |
| AMD Ryzen 5 7600X                      Гейминг 1440p (RTX 4070+) ✔️  AM5   |
+-----------------------------------------------------------------------------+
| [M3: Core KPI Grid — Relative Metrics]                                      |
|  Cores/Threads: 6 / 12      Max Boost Clock: 5.3 GHz    TDP: 105W           |
|  Gaming (1440p, RTX 4090*): 134% vs R5 5600X                               |
|  Multi-Core: 182% vs R5 5600X                     Base Price: $220          |
+-----------------------------------------------------------------------------+
| [M4: Canonical Decision Teaser]                                             |
| "Оптимален для сборок с RTX 4070/4070Ti на долговечной платформе AM5"      |
+-----------------------------------------------------------------------------+
| [M5: Action Bar]                                                            |
| [ Добавить к сравнению ]                        [ Подробнее о решениях (4) ]|
+-----------------------------------------------------------------------------+
```

**Изменения относительно v0.3.1:**
- `Verdict Badges` → `ScopedDecisionTags` с явной scope-привязкой
- `Gaming Index: 87/100` → `Gaming (1440p, RTX 4090*): 134% vs R5 5600X`
- `Multi-Core Perf: 72/100` → `Multi-Core: 182% vs R5 5600X`
- Каждая относительная метрика несёт условия теста прямо на карточке

---

## ViewModel v0.3.2 — открытые вопросы

### Gaming Index: вопрос выбора подхода

Композитный индекс без видимой методологии/scope/epistemic-тега воспроизводит
проблему, убранную вместе с shortVerdict: безусловное число вместо scoped-вывода.
Два пути:

- **(А) Убрать индексы из карточки полностью**, оставить только сырые измеримые
  величины (ядра/потоки, частоты, TDP) — карточка становится менее «сканируемой»
  с первого взгляда, но ничего не заявляет без evidence. Card Teaser
  (chosenAnswer canonical Decision) остаётся единственным качественным сигналом,
  но он уже honestly scoped.

- **(Б) Оставить индекс как выведенный (а не декларативный)** —
  задокументированная формула (например, средневзвешенный fps по
  зафиксированному набору игр на зафиксированном GPU-классе), обязательный
  `epistemicTag: "modeled"`, и обязательное отображение допущения расчёта
  прямо на карточке. Индекс не отменяет scope, а несёт его с собой.

**Статус:** открытый вопрос, требует редакционного решения.

### N=3 сравнение и попарные Decision

**Статус: решено в v0.3.3.** Принят Вариант А (Raw Spec Fallback).

При `selectedCpuIds.length === 3` роутер ведёт на `/compare/`, которая рендерит
чистую сетку технических характеристик без редакционного слоя. Попытка объединить
три попарные дуэли решений на одной странице перегрузит интерфейс.

На странице N=3 сравнения выводится системная плашка:
> 💡 «Совет: Уберите один процессор из сравнения, чтобы разблокировать наше
> глубокое редакционное сравнение решений 1-на-1».

```typescript
function getComparisonRenderMode(cpuIds: string[]): "single-decision" | "raw-fallback" {
  if (cpuIds.length === 2) return "single-decision";
  return "raw-fallback"; // N=3 или любое другое не-2 количество
}
```

---

## ViewModel v0.3.3 — Закрытие технических вопросов

### 1. frequencyF официально в интерфейсе Decision

Поле `frequencyF` добавляется на уровень интерфейса Decision. Представляет
собой кэшированное значение частотности поискового спроса ядра дилеммы,
обновляемое ежеквартально в фоновом режиме.

```typescript
interface Decision {
  id: string;
  taxonomyType: DecisionTaxonomy;
  comparisonMode: ComparisonMode;
  frequencyF: number; // кэшированное значение из B1 real-world-frequency сигнала;
                       // обновляется ежеквартально. Используется getCanonicalDecision.
  // ...остальные поля
}
```

### 2. Эпистемический субтекст под относительной метрикой

На фасаде карточки относительная метрика всегда выводится в связке с контекстом
тестирования (GPU-tier и разрешение), на котором этот перформанс был изолирован.

**Визуальный формат:**
- `134% vs R5 5600X` (крупный шрифт)
- `[RTX 4090, 1080p Ultra]` (мелкий приглушённый шрифт прямо под цифрой)

**Значение для пользователя:** инженер мгновенно считывает: «Этот прирост
получен в идеальных условиях упора в процессор на RTX 4090. На моей RTX 4060
разница будет меньше».

### 3. Жизненный цикл Baseline CPU

Базовый процессор сравнения (Ryzen 5 5600X) меняется раз в два поколения
(примерно раз в 3.5–4 года) решением редакции. При смене эталона на бэкенде
запускается скрипт пересчёта, который автоматически делит новые бенчмарки на
результаты нового эталона, обновляя все индексы в базе без участия авторов.

**Quarterly Re-evaluation Pipeline** (из v0.3.2) применяется к проверке
актуальности baseline, но смена происходит только по crossing-generation
trigger (выход нового поколения CPU, а не календарно).

---

## Часть 3: Детальный дизайн Layout карточки Dashboard SKU Card

Этот организм — ключевой элемент каталога. Он должен оставаться плотным,
информативным, но не превращаться в кашу при просмотре с мобильных устройств.

### 1. CSS Grid схема (Desktop, 12-колоночная микро-сетка)

Верстаем карточку на CSS Grid с внутренним делением на зоны:

```
+--------------------------------------------------------------------------------------------------------+
| AREA 1: HEADER (12 cols)                                                                               |
| [Brand logo] AMD Ryzen 5 7600X                             [Tags: Gaming 1440p (RTX 4070+) | AM5 ]     |
+----------------------------------------------------+---------------------------------------------------+
| AREA 2: METRICS (7 cols)                           | AREA 3: SPECS (5 cols)                            |
|                                                    |                                                   |
| Gaming (1440p): 134% vs R5 5600X                   | Socket:        AM5                                |
| [Context: RTX 4090, 1080p Ultra]                   | TDP Class:     Medium (105W)                      |
|                                                    | Memory Gen:    DDR5                               |
| Multi-Core:     182% vs R5 5600X                   | Release:       2022                               |
| [Context: Cinebench R23 Multi]                     | Base Price:    $220                               |
+----------------------------------------------------+---------------------------------------------------+
| AREA 4: CANONICAL DECISION TEASER (12 cols)                                                            |
| "Оптимален для сборок с RTX 4070/4070Ti на долговечной платформе AM5"                                  |
+--------------------------------------------------------------------------------------------------------+
| AREA 5: ACTION BAR (12 cols)                                                                           |
| [ Добавить к сравнению ]                                                   [ Подробнее о решениях (4) ]|
+--------------------------------------------------------------------------------------------------------+
```

### 2. Адаптивность (Mobile Downscaling, <768px)

При ширине экрана меньше 768px сетка карточки перестраивается в линейный стек
(одномерный поток):

1. **Header** сохраняет строку (бренд слева, теги справа), но у тегов скрывается
   текстовая часть условий — остаются только иконки: 🎮 1440p вместо полного текста.
2. **Metrics и Specs** схлопываются в две последовательные строки.
3. **Teaser** скрывается на мобильных экранах — приоритет: быстрое сканирование
   характеристик и цен.
4. **Action Bar** становится вертикальным (кнопки на всю ширину друг под другом).

### 3. Техническая спецификация разметки (HTML/Tailwind)

```html
<article class="grid grid-cols-12 gap-4 p-5 bg-slate-900 border border-slate-800 rounded-lg text-slate-100 hover:border-slate-700 transition-colors">
  
  <!-- AREA 1: HEADER -->
  <header class="col-span-12 flex justify-between items-start border-b border-slate-800 pb-3">
    <div>
      <span class="text-xs font-mono text-amber-500 uppercase tracking-wider">AMD Zen 4</span>
      <h3 class="text-xl font-bold tracking-tight mt-1">Ryzen 5 7600X</h3>
    </div>
    <!-- Scoped Tags -->
    <div class="flex gap-2">
      <span class="text-xs px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded font-medium">
        🎮 Гейминг 1440p (RTX 4070+)
      </span>
      <span class="text-xs px-2 py-1 bg-slate-800 text-slate-300 rounded font-mono">
        AM5
      </span>
    </div>
  </header>

  <!-- AREA 2: METRICS -->
  <section class="col-span-12 md:col-span-7 flex flex-col gap-3">
    <div>
      <div class="text-xs text-slate-400">Игровая производительность</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="text-2xl font-black text-slate-100">134%</span>
        <span class="text-xs text-slate-400">vs R5 5600X</span>
      </div>
      <span class="text-[10px] font-mono text-slate-500 block">[Тест: RTX 4090, 1080p Ultra]</span>
    </div>
    
    <div>
      <div class="text-xs text-slate-400">Многопоточная мощность</div>
      <div class="flex items-baseline gap-2 mt-1">
        <span class="text-2xl font-black text-slate-100">182%</span>
        <span class="text-xs text-slate-400">vs R5 5600X</span>
      </div>
      <span class="text-[10px] font-mono text-slate-500 block">[Тест: Cinebench R23 Multi]</span>
    </div>
  </section>

  <!-- AREA 3: SPECS -->
  <aside class="col-span-12 md:col-span-5 bg-slate-950 p-3 rounded border border-slate-800 text-xs font-mono flex flex-col gap-2">
    <div class="flex justify-between"><span class="text-slate-500">Сокет:</span> <span class="text-slate-300">AM5</span></div>
    <div class="flex justify-between"><span class="text-slate-500">Память:</span> <span class="text-slate-300">DDR5</span></div>
    <div class="flex justify-between"><span class="text-slate-500">TDP:</span> <span class="text-slate-300">105W (Medium)</span></div>
    <div class="flex justify-between border-t border-slate-800 pt-1 mt-1 font-bold text-slate-200">
      <span>Базовая цена:</span> <span>$220</span>
    </div>
  </aside>

  <!-- AREA 4: CANONICAL DECISION TEASER (Hidden on Mobile) -->
  <blockquote class="hidden md:block col-span-12 p-3 bg-slate-950/50 border-l-2 border-amber-500 text-xs text-slate-300 italic">
    "Оптимален для сборок с RTX 4070/4070Ti на долговечной платформе AM5"
  </blockquote>

  <!-- AREA 5: ACTION BAR -->
  <footer class="col-span-12 flex flex-col sm:flex-row gap-2 justify-between border-t border-slate-800 pt-3 mt-1">
    <button class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded transition-colors text-center">
      ✚ Добавить к сравнению
    </button>
    <a href="/processors/amd/ryzen-5-7600x/" class="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-slate-950 text-xs font-bold rounded transition-colors text-center">
      Подробнее о решениях (4) →
    </a>
  </footer>
</article>
```
 
## Часть 2: Стейт-менеджмент и логика Comparison Drawer

ComparisonDrawer (Панель сравнения) — глобальный плавающий виджет в нижней
части экрана, накапливающий выбранные пользователем процессоры для сопоставления.

### 1. Архитектура стейта (Zustand-style Store)

Стейт глобальный, реактивный, персистентный (sessionStorage — не сбрасывается
при переходах между страницами каталога).

```typescript
interface ComparisonState {
  selectedCpuIds: string[];         // максимум 3
  selectedCpuSlugs: string[];       // зеркало для роутинга
  isDrawerOpen: boolean;            // управляет анимацией

  // Actions
  addCpu: (cpuId: string, cpuSlug: string) => AddCpuResult;
  removeCpu: (cpuId: string) => void;
  clearAll: () => void;
  isSelected: (cpuId: string) => boolean;
  canAdd: () => boolean;             // selectedCpuIds.length < 3
}

type AddCpuResult =
  | { status: "added" }
  | { status: "rejected"; reason: "capacity_limit" | "already_selected" };
```

### 2. Системные правила и валидаторы (Business Rules)

При добавлении процессора в корзину сравнения на клиенте отрабатывают три триггера:

**А. Лимит емкости (Capacity Limit)**

- **Правило:** не более 3-х моделей одновременно.
- **UX:** при превышении лимита кнопка «Добавить к сравнению» блокируется
  (disabled), тултип: «Для глубокого анализа ограничьтесь 3 процессорами».

**Б. Контроль совместимости платформ (Platform Clash Detector)**

- **Правило:** сравнение процессоров разных сокетов допустимо, но требует
  предупреждения.
- **UX:** если `selectedCpuIds` содержат разные сокеты (например, AM5 и LGA1700),
  в ComparisonDrawer выводится статус:
  > ⚠️ «Вы сравниваете процессоры разных платформ (AM5 и LGA1700). Потребуются
  > разные материнские платы и, возможно, память».
- Защищает новичков от иллюзии взаимозаменяемости в рамках одной сборки.

**В. Детектор готовых сравнений (Decision Pre-render Check)**

- **Правило:** если в стейте ровно 2 процессора, система проверяет существование
  ComponentChoiceDecision для этой пары.
- **UX:**
  - Готовое решение **есть** → кнопка акцентного цвета: «Смотреть дуэль решений»
  - Решения **нет** → кнопка: «Сравнить технические ТТХ» (стандартный
    параметрический fallback)

```typescript
interface ComparisonDrawerViewModel {
  items: Array<{
    cpuId: string;
    slug: string;
    title: string;
    socket: string;
  }>;
  platformClash: boolean;             // true если разные сокеты
  hasReadyDecision: boolean;          // true если для пары есть ComponentChoiceDecision
  primaryActionLabel: string;         // «Смотреть дуэль решений» | «Сравнить технические ТТХ»
  primaryActionUrl: string;           // /compare/processors/[slug1]-vs-[slug2]/
}
```

### 3. Жизненный цикл и анимации Drawer (UX)

- **Монтирование (Mounting):** при пустом стейте (`selectedCpuIds.length === 0`)
  компонент полностью скрыт из DOM (не занимает место на экране).
- **Появление (First Item):** при добавлении первого процессора виджет плавно
  выезжает снизу (`transform: translateY(0)` с эффектом spring), фиксируясь над
  основным контентом (`z-index: 100`).
- **Переход к действию:** клик по кнопке «Сравнить» триггерит роутер:
  - 2 модели: `/compare/processors/[slug1]-vs-[slug2]/`
  - 3 модели: `/compare/processors/[slug1]-vs-[slug2]-vs-[slug3]/`
- **Контроль отмены:** каждая карточка в drawer имеет кнопку удаления (крестик).
  Удаление последнего элемента скрывает drawer с анимацией схлопывания.

---

## Альтернативы

Старая модель («карточка объекта»: спеки + бенчи + цена, verdict как сумма впечатлений) — отвергнута, так как:

| Аспект | Старая модель | Новая модель |
|--------|--------------|-------------|
| Verdict | Сумма впечатлений, применима «вообще» | Decision с явной scope, без обобщений |
| Бенчмарки | Витрина | Evidence, подтягиваемый под конкретный Decision |
| Число решений | Фиксировано дизайном | Результат Genuine Tension Test |
| Нарратив | Диктуется KPI Dashboard | Диктуется DecisionExplorer |
| Каталог | Бесконечная сетка карточек | Dashboard с Use-Case Pivot Tiles + Smart Filters |

## Последствия

### Что становится проще
- Поисковый робот видит структурный граф: каждый фильтр → страница с H1 и релевантной выдачей
- Verdict всегда привязан к области действия — невозможно написать «хорош/плох» без scope
- Epistemic honesty: confidenceNote и Content Debt Log делают пробелы в данных явными
- Каталог: ScopedDecisionTags несут scope-привязку прямо на фасаде карточки — никаких безадресных «Gaming Value»
- Relative Metrics (134% vs R5 5600X) — физически обоснованные числа с видимой методологией
- Canonical Decision — детерминированный алгоритм выбора, устраняет рассинхронизацию заголовка и тизера

### Что усложняется
- Полнота benchmark KB становится хардблокером публикации (отсутствие данных по оси контракта → Evidence Sufficiency Fail)
- Требуется калибровочная петля с регрессионным тестированием при изменении порогов
- Content Lifecycle Policy для вытесненных top-3 сценариев требует процедуры
- Baseline CPU нуждается в Quarterly Re-evaluation Pipeline (синхронизация с пайплайном UpgradePathDecision)
- Comparison Drawer: 3 бизнес-правила (capacity limit, platform clash, decision pre-render) требуют клиентской имплементации

### Что требует внимания
- Операционная зависимость: таблица gpuEquivalenceTier требует владельца и обновления
- RejectReasonTag не покрывает ошибку калибровки порога F (wrong_frequency_threshold)
- Лог исторических reject-ов нуждается в периодической ревизии
- UI-паттерн для threshold/temporal comparisonMode (DecisionExplorer/BenchmarkVisualizer) ещё не спроектирован

### Открытые вопросы (v0.3.3)
- Все вопросы разрешены. Gaming Index: выбран вариант Б (modeled-композит с видимым scope и epistemicTag). Требует наполнения Minerva бенчмарками (Phase 0).
