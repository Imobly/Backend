# 📊 Dashboard API - Referência Completa

## Visão Geral

O Dashboard API oferece endpoints robustos para visualização e análise de dados da plataforma de gestão imobiliária. Todos os endpoints são **filtrados automaticamente por usuário** (multi-tenancy) e suportam filtros adicionais por período, propriedade e outros parâmetros.

### 🔐 Autenticação

Todos os endpoints requerem autenticação via JWT Bearer token no header:

```http
Authorization: Bearer {seu_token_jwt}
```

---

## 📈 Endpoints Disponíveis

### 1. Estatísticas Básicas

**Endpoint:** `GET /api/v1/dashboard/stats`

Retorna estatísticas básicas do usuário autenticado.

**Resposta:**
```json
{
  "total_properties": 1,
  "total_tenants": 1,
  "total_contracts": 1,
  "monthly_revenue": 2500.0
}
```

**Campos:**
- `total_properties`: Número total de imóveis do usuário
- `total_tenants`: Número total de inquilinos cadastrados
- `total_contracts`: Número de contratos ativos
- `monthly_revenue`: Receita mensal esperada (soma dos aluguéis ativos)

**Uso (TypeScript/React):**
```typescript
interface DashboardStats {
  total_properties: number;
  total_tenants: number;
  total_contracts: number;
  monthly_revenue: number;
}

const fetchStats = async (): Promise<DashboardStats> => {
  const response = await api.get('/dashboard/stats');
  return response.data;
};
```

---

### 2. Resumo Completo

**Endpoint:** `GET /api/v1/dashboard/summary`

Visão geral completa com informações financeiras e de contratos.

**Resposta:**
```json
{
  "properties": {
    "total": 1,
    "active_contracts": 1
  },
  "contracts": {
    "active": 1,
    "expiring_soon": 0
  },
  "financial": {
    "monthly_revenue": 2500.0,
    "overdue_payments": 0,
    "pending_payments": 0
  }
}
```

**Campos:**
- `properties.total`: Total de imóveis
- `properties.active_contracts`: Imóveis com contratos ativos
- `contracts.active`: Total de contratos ativos
- `contracts.expiring_soon`: Contratos vencendo nos próximos 30 dias
- `financial.monthly_revenue`: Receita mensal esperada
- `financial.overdue_payments`: Número de pagamentos em atraso
- `financial.pending_payments`: Número de pagamentos pendentes

---

### 3. Gráfico de Receitas

**Endpoint:** `GET /api/v1/dashboard/revenue-chart?months={n}`

Dados para gráfico de evolução de receitas ao longo do tempo.

**Query Parameters:**
- `months` (opcional, padrão: 12): Número de meses (1-24)

**Resposta:**
```json
{
  "data": [
    {
      "month": "2025-06",
      "revenue": 0.0
    },
    {
      "month": "2025-07",
      "revenue": 0.0
    },
    {
      "month": "2025-11",
      "revenue": 2754.17
    }
  ]
}
```

**Exemplo de uso com Chart.js:**
```typescript
import { Line } from 'react-chartjs-2';

const RevenueChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    api.get('/dashboard/revenue-chart?months=6')
      .then(response => {
        setChartData({
          labels: response.data.data.map(d => d.month),
          datasets: [{
            label: 'Receitas',
            data: response.data.data.map(d => d.revenue),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        });
      });
  }, []);

  return chartData ? <Line data={chartData} /> : <p>Carregando...</p>;
};
```

---

### 4. 💰 Receitas vs Despesas (NOVO)

**Endpoint:** `GET /api/v1/dashboard/revenue-vs-expenses?months={n}&property_id={id}`

Dados comparativos de receitas, despesas e lucro líquido ao longo do tempo.

**Query Parameters:**
- `months` (opcional, padrão: 12): Número de meses (1-24)
- `property_id` (opcional): Filtrar por propriedade específica

**Resposta:**
```json
{
  "data": [
    {
      "month": "2025-06",
      "revenue": 0.0,
      "expenses": 0.0,
      "profit": 0.0
    },
    {
      "month": "2025-11",
      "revenue": 2754.17,
      "expenses": 250.0,
      "profit": 2504.17
    }
  ]
}
```

**Campos:**
- `revenue`: Total de receitas (pagamentos recebidos) no mês
- `expenses`: Total de despesas no mês
- `profit`: Lucro líquido (receitas - despesas)

**Exemplo com gráfico de barras (Chart.js):**
```typescript
import { Bar } from 'react-chartjs-2';

const RevenueExpensesChart = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get('/dashboard/revenue-vs-expenses?months=6')
      .then(response => {
        const chartData = response.data.data;
        setData({
          labels: chartData.map(d => d.month),
          datasets: [
            {
              label: 'Receitas',
              data: chartData.map(d => d.revenue),
              backgroundColor: 'rgba(75, 192, 192, 0.5)',
            },
            {
              label: 'Despesas',
              data: chartData.map(d => d.expenses),
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
              label: 'Lucro',
              data: chartData.map(d => d.profit),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
            }
          ]
        });
      });
  }, []);

  return data ? <Bar data={data} /> : <p>Carregando...</p>;
};
```

---

### 5. 📊 Visão Geral Financeira (NOVO)

**Endpoint:** `GET /api/v1/dashboard/financial-overview?start_date={date}&end_date={date}&property_id={id}`

Análise financeira detalhada com breakdown de despesas por categoria e status de pagamentos.

**Query Parameters:**
- `start_date` (opcional, formato: YYYY-MM-DD): Data inicial do período
- `end_date` (opcional, formato: YYYY-MM-DD): Data final do período
- `property_id` (opcional): Filtrar por propriedade específica

**Se as datas não forem fornecidas, usa o mês atual como padrão.**

**Resposta:**
```json
{
  "period": {
    "start_date": "2025-11-01",
    "end_date": "2025-11-30"
  },
  "summary": {
    "total_revenue": 2754.17,
    "total_expenses": 250.0,
    "net_profit": 2504.17,
    "profit_margin": 90.92
  },
  "expense_breakdown": [
    {
      "category": "IPTU",
      "amount": 250.0
    },
    {
      "category": "Manutenção",
      "amount": 150.0
    }
  ],
  "payment_status": {
    "paid": 1,
    "pending": 0,
    "overdue": 0,
    "partial": 0
  },
  "filters_applied": {
    "property_id": null
  }
}
```

**Campos:**
- `summary.total_revenue`: Total de receitas no período
- `summary.total_expenses`: Total de despesas no período
- `summary.net_profit`: Lucro líquido
- `summary.profit_margin`: Margem de lucro (%)
- `expense_breakdown`: Lista de despesas agrupadas por categoria
- `payment_status`: Contagem de pagamentos por status

**Exemplo de uso:**
```typescript
interface FinancialOverview {
  period: {
    start_date: string;
    end_date: string;
  };
  summary: {
    total_revenue: number;
    total_expenses: number;
    net_profit: number;
    profit_margin: number;
  };
  expense_breakdown: Array<{
    category: string;
    amount: number;
  }>;
  payment_status: {
    paid: number;
    pending: number;
    overdue: number;
    partial: number;
  };
}

// Filtrar por período específico
const getFinancialOverview = async (
  startDate: string,
  endDate: string,
  propertyId?: number
): Promise<FinancialOverview> => {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
  });
  
  if (propertyId) {
    params.append('property_id', propertyId.toString());
  }
  
  const response = await api.get(`/dashboard/financial-overview?${params}`);
  return response.data;
};

// Exemplo de gráfico de pizza para despesas
const ExpensesPieChart = ({ data }: { data: FinancialOverview }) => {
  const chartData = {
    labels: data.expense_breakdown.map(e => e.category),
    datasets: [{
      data: data.expense_breakdown.map(e => e.amount),
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
      ]
    }]
  };
  
  return <Pie data={chartData} />;
};
```

---

### 6. 🏠 Status dos Imóveis (NOVO)

**Endpoint:** `GET /api/v1/dashboard/properties-status`

Status detalhado de todos os imóveis do usuário, incluindo ocupação, receitas e despesas.

**Resposta:**
```json
{
  "summary": {
    "total_properties": 1,
    "occupied": 1,
    "vacant": 0,
    "occupancy_rate": 100.0
  },
  "properties": [
    {
      "id": 2,
      "name": "apt samambaia",
      "address": "Quadra 403, apt 702",
      "type": "apartment",
      "status": "occupied",
      "active_contracts": 1,
      "expected_monthly_revenue": 2500.0,
      "received_monthly_revenue": 2754.17,
      "monthly_expenses": 250.0,
      "net_profit": 2504.17
    }
  ]
}
```

**Campos:**
- `summary.occupancy_rate`: Taxa de ocupação (%)
- `properties[].status`: `"occupied"` ou `"vacant"`
- `properties[].expected_monthly_revenue`: Receita esperada (soma dos aluguéis)
- `properties[].received_monthly_revenue`: Receita recebida no mês atual
- `properties[].monthly_expenses`: Despesas do mês atual
- `properties[].net_profit`: Lucro líquido do imóvel

**Exemplo de uso:**
```typescript
interface PropertyStatus {
  id: number;
  name: string;
  address: string;
  type: string;
  status: 'occupied' | 'vacant';
  active_contracts: number;
  expected_monthly_revenue: number;
  received_monthly_revenue: number;
  monthly_expenses: number;
  net_profit: number;
}

interface PropertiesStatusResponse {
  summary: {
    total_properties: number;
    occupied: number;
    vacant: number;
    occupancy_rate: number;
  };
  properties: PropertyStatus[];
}

// Componente de lista de imóveis
const PropertiesList = () => {
  const [data, setData] = useState<PropertiesStatusResponse | null>(null);

  useEffect(() => {
    api.get('/dashboard/properties-status')
      .then(response => setData(response.data));
  }, []);

  if (!data) return <p>Carregando...</p>;

  return (
    <div>
      <div className="summary">
        <h3>Resumo</h3>
        <p>Taxa de Ocupação: {data.summary.occupancy_rate}%</p>
        <p>Ocupados: {data.summary.occupied} / {data.summary.total_properties}</p>
      </div>
      
      <div className="properties-grid">
        {data.properties.map(property => (
          <div key={property.id} className="property-card">
            <h4>{property.name}</h4>
            <p>Status: {property.status === 'occupied' ? '✅ Ocupado' : '⚠️ Vago'}</p>
            <p>Receita: R$ {property.received_monthly_revenue.toFixed(2)}</p>
            <p>Despesas: R$ {property.monthly_expenses.toFixed(2)}</p>
            <p>Lucro: R$ {property.net_profit.toFixed(2)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

### 7. Performance das Propriedades

**Endpoint:** `GET /api/v1/dashboard/property-performance`

Performance individual de cada imóvel com taxa de cobrança.

**Resposta:**
```json
{
  "properties": [
    {
      "property_id": 2,
      "property_name": "apt samambaia",
      "property_address": "Quadra 403, apt 702",
      "active_contracts": 1,
      "revenue_received": 2754.17,
      "revenue_expected": 2500.0,
      "collection_rate": 110.17
    }
  ]
}
```

**Campos:**
- `collection_rate`: Taxa de cobrança (%) = (receita recebida / receita esperada) × 100

---

### 8. Atividades Recentes

**Endpoint:** `GET /api/v1/dashboard/recent-activity?limit={n}`

Lista as atividades recentes do usuário (pagamentos e contratos).

**Query Parameters:**
- `limit` (opcional, padrão: 10): Número máximo de atividades (1-50)

**Resposta:**
```json
{
  "activities": [
    {
      "type": "payment",
      "description": "Pagamento de R$ 2754.17 - Status: paid",
      "date": "2025-11-28",
      "related_id": 6,
      "created_at": "2025-11-23 14:12:43.875610"
    },
    {
      "type": "contract",
      "description": "Contrato criado - Status: active",
      "date": "2025-06-14",
      "related_id": 3,
      "created_at": "2025-11-22 18:55:31.923258"
    }
  ]
}
```

---

## 🎨 Exemplos de Implementação Frontend

### Dashboard Completo (React)

```typescript
import { useState, useEffect } from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import api from './api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [revenueVsExpenses, setRevenueVsExpenses] = useState(null);
  const [financialOverview, setFinancialOverview] = useState(null);
  const [propertiesStatus, setPropertiesStatus] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsRes, revenueRes, financialRes, propertiesRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/dashboard/revenue-vs-expenses?months=6'),
        api.get('/dashboard/financial-overview'),
        api.get('/dashboard/properties-status')
      ]);

      setStats(statsRes.data);
      setRevenueVsExpenses(revenueRes.data);
      setFinancialOverview(financialRes.data);
      setPropertiesStatus(propertiesRes.data);
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
    }
  };

  if (!stats) return <div>Carregando...</div>;

  return (
    <div className="dashboard">
      {/* Cards de Estatísticas */}
      <div className="stats-cards">
        <div className="card">
          <h3>Imóveis</h3>
          <p className="big-number">{stats.total_properties}</p>
        </div>
        <div className="card">
          <h3>Contratos Ativos</h3>
          <p className="big-number">{stats.total_contracts}</p>
        </div>
        <div className="card">
          <h3>Receita Mensal</h3>
          <p className="big-number">R$ {stats.monthly_revenue.toFixed(2)}</p>
        </div>
      </div>

      {/* Gráfico Receitas vs Despesas */}
      {revenueVsExpenses && (
        <div className="chart-container">
          <h2>Receitas vs Despesas (6 meses)</h2>
          <Bar
            data={{
              labels: revenueVsExpenses.data.map(d => d.month),
              datasets: [
                {
                  label: 'Receitas',
                  data: revenueVsExpenses.data.map(d => d.revenue),
                  backgroundColor: 'rgba(75, 192, 192, 0.5)',
                },
                {
                  label: 'Despesas',
                  data: revenueVsExpenses.data.map(d => d.expenses),
                  backgroundColor: 'rgba(255, 99, 132, 0.5)',
                }
              ]
            }}
          />
        </div>
      )}

      {/* Resumo Financeiro */}
      {financialOverview && (
        <div className="financial-summary">
          <h2>Resumo Financeiro (Mês Atual)</h2>
          <div className="summary-cards">
            <div className="card green">
              <h4>Receitas</h4>
              <p>R$ {financialOverview.summary.total_revenue.toFixed(2)}</p>
            </div>
            <div className="card red">
              <h4>Despesas</h4>
              <p>R$ {financialOverview.summary.total_expenses.toFixed(2)}</p>
            </div>
            <div className="card blue">
              <h4>Lucro Líquido</h4>
              <p>R$ {financialOverview.summary.net_profit.toFixed(2)}</p>
            </div>
            <div className="card purple">
              <h4>Margem</h4>
              <p>{financialOverview.summary.profit_margin}%</p>
            </div>
          </div>
        </div>
      )}

      {/* Status dos Imóveis */}
      {propertiesStatus && (
        <div className="properties-overview">
          <h2>Status dos Imóveis</h2>
          <p>Taxa de Ocupação: {propertiesStatus.summary.occupancy_rate}%</p>
          <div className="properties-grid">
            {propertiesStatus.properties.map(property => (
              <div key={property.id} className="property-card">
                <h3>{property.name}</h3>
                <p className="status">{property.status === 'occupied' ? '✅ Ocupado' : '⚠️ Vago'}</p>
                <p>Receita: R$ {property.received_monthly_revenue.toFixed(2)}</p>
                <p>Despesas: R$ {property.monthly_expenses.toFixed(2)}</p>
                <p className="profit">Lucro: R$ {property.net_profit.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
```

---

## 🔍 Filtros Disponíveis

### Por Período
Disponível em: `/financial-overview`

```typescript
// Filtrar por período customizado
const data = await api.get('/dashboard/financial-overview', {
  params: {
    start_date: '2025-01-01',
    end_date: '2025-12-31'
  }
});
```

### Por Propriedade
Disponível em: `/revenue-vs-expenses`, `/financial-overview`

```typescript
// Filtrar por propriedade específica
const data = await api.get('/dashboard/revenue-vs-expenses', {
  params: {
    months: 12,
    property_id: 2
  }
});
```

### Por Número de Meses
Disponível em: `/revenue-chart`, `/revenue-vs-expenses`

```typescript
// Últimos 3 meses
const data = await api.get('/dashboard/revenue-vs-expenses?months=3');

// Últimos 24 meses
const data = await api.get('/dashboard/revenue-vs-expenses?months=24');
```

---

## 🎯 Casos de Uso

### 1. Dashboard Principal
Combine `/stats`, `/summary` e `/revenue-vs-expenses` para criar um dashboard completo com visão geral + gráficos.

### 2. Análise Financeira
Use `/financial-overview` para relatórios detalhados com breakdown de despesas por categoria.

### 3. Gestão de Imóveis
Use `/properties-status` para visualizar status de ocupação e performance individual de cada imóvel.

### 4. Comparação Temporal
Use `/revenue-vs-expenses` com diferentes valores de `months` para análise de tendências ao longo do tempo.

### 5. Relatório por Imóvel
Aplique o filtro `property_id` em `/financial-overview` e `/revenue-vs-expenses` para análise específica de um imóvel.

---

## ⚠️ Observações Importantes

1. **Multi-tenancy**: Todos os dados são automaticamente filtrados pelo `user_id` do token JWT. Um usuário nunca verá dados de outro usuário.

2. **Performance**: Para gráficos com muitos meses, considere usar cache no frontend ou limitar a quantidade inicial de dados carregados.

3. **Datas**: Sempre use formato ISO (YYYY-MM-DD) para datas nos filtros.

4. **Valores monetários**: Todos os valores são retornados como `float`. No frontend, use `.toFixed(2)` para formatação.

5. **Status de pagamentos**: Os status possíveis são: `paid`, `pending`, `overdue`, `partial`.

---

## 🚀 Próximos Passos

Para integrar o dashboard no seu frontend:

1. Configure o interceptor do axios com o token JWT
2. Crie componentes reutilizáveis para cada tipo de gráfico
3. Implemente loading states e tratamento de erros
4. Adicione opções de filtros (seletor de período, dropdown de propriedades)
5. Considere usar React Query ou SWR para cache e revalidação automática
