import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './pages/Login'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  const [count, setCount] = useState(0)

  return <>
  <BrowserRouter>
  <Routes>
    <Route path='/' element={<div>Home</div>}></Route>
    <Route path='/login' element={Login}></Route>
    <Route path='/register' element={Register}></Route>
  </Routes>
  </BrowserRouter>
  </>
}

export default App
