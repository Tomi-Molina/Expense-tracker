import { Navigate, Route, Routes, Link, useNavigate } from 'react-router-dom'
import { useEffect, useMemo, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function apiRequest(path, { method = 'GET', body, token } = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || 'Something went wrong')
  }
  return data
}

function AuthPage({ mode }) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const title = mode === 'login' ? 'Login' : 'Register'

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await apiRequest(`/auth/${mode}`, {
        method: 'POST',
        body: { email, password },
      })
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-screen">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <h1>{title}</h1>
        <p className="muted">Expense Tracker portfolio project</p>
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label>
          Password
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required minLength={6} />
        </label>
        {error ? <div className="error">{error}</div> : null}
        <button className="primary-btn" type="submit" disabled={loading}>
          {loading ? 'Please wait...' : title}
        </button>
        <div className="auth-links">
          {mode === 'login' ? (
            <Link to="/register">Need an account? Register</Link>
          ) : (
            <Link to="/login">Already have an account? Login</Link>
          )}
        </div>
      </form>
    </div>
  )
}

function Dashboard() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')
  const user = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('user') || 'null')
    } catch {
      return null
    }
  }, [])

  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState({
    amount: '',
    category: '',
    date: '',
    description: '',
  })

  async function loadExpenses() {
    setLoading(true)
    setError('')
    try {
      const data = await apiRequest('/expenses', { token })
      setExpenses(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!token) {
      navigate('/login')
      return
    }
    loadExpenses()
  }, [token])

  function resetForm() {
    setEditingId(null)
    setForm({ amount: '', category: '', date: '', description: '' })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const payload = {
        amount: Number(form.amount),
        category: form.category,
        date: form.date,
        description: form.description,
      }

      if (editingId) {
        await apiRequest(`/expenses/${editingId}`, { method: 'PUT', body: payload, token })
      } else {
        await apiRequest('/expenses', { method: 'POST', body: payload, token })
      }

      resetForm()
      await loadExpenses()
    } catch (err) {
      setError(err.message)
    }
  }

  function startEdit(expense) {
    setEditingId(expense.id)
    setForm({
      amount: expense.amount,
      category: expense.category,
      date: String(expense.date).slice(0, 10),
      description: expense.description,
    })
  }

  async function deleteExpense(id) {
    if (!confirm('Delete this expense?')) return
    try {
      await apiRequest(`/expenses/${id}`, { method: 'DELETE', token })
      await loadExpenses()
    } catch (err) {
      setError(err.message)
    }
  }

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  const total = expenses.reduce((sum, expense) => sum + Number(expense.amount), 0)

  return (
    <div className="page">
      <header className="topbar card">
        <div>
          <h1>Expense Tracker</h1>
          <p className="muted">Welcome{user?.email ? `, ${user.email}` : ''}</p>
        </div>
        <button className="secondary-btn" onClick={logout}>Logout</button>
      </header>

      <section className="grid">
        <form className="card" onSubmit={handleSubmit}>
          <h2>{editingId ? 'Edit expense' : 'Add expense'}</h2>
          <label>
            Amount
            <input
              value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              type="number"
              step="0.01"
              required
            />
          </label>
          <label>
            Category
            <input
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
              required
            />
          </label>
          <label>
            Date
            <input
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              type="date"
              required
            />
          </label>
          <label>
            Description
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              rows="4"
              required
            />
          </label>
          {error ? <div className="error">{error}</div> : null}
          <div className="row">
            <button className="primary-btn" type="submit">
              {editingId ? 'Update' : 'Create'}
            </button>
            {editingId ? (
              <button className="secondary-btn" type="button" onClick={resetForm}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <div className="card">
          <div className="summary">
            <div>
              <h2>Expenses</h2>
              <p className="muted">{expenses.length} record(s)</p>
            </div>
            <div className="total-box">
              <span>Total</span>
              <strong>${total.toFixed(2)}</strong>
            </div>
          </div>

          {loading ? (
            <p className="muted">Loading...</p>
          ) : expenses.length === 0 ? (
            <p className="muted">No expenses yet.</p>
          ) : (
            <div className="expense-list">
              {expenses.map((expense) => (
                <article className="expense-item" key={expense.id}>
                  <div>
                    <div className="expense-title">
                      <strong>${Number(expense.amount).toFixed(2)}</strong>
                      <span>{expense.category}</span>
                    </div>
                    <p className="muted">{expense.description}</p>
                    <small>{String(expense.date).slice(0, 10)}</small>
                  </div>
                  <div className="row">
                    <button className="secondary-btn" onClick={() => startEdit(expense)}>Edit</button>
                    <button className="danger-btn" onClick={() => deleteExpense(expense.id)}>Delete</button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<AuthPage mode="login" />} />
      <Route path="/register" element={<AuthPage mode="register" />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
