import React, {useEffect, useState} from 'react'

const API = 'http://localhost:8000'

export default function App(){
    const [health, setHealth] = useState(null)
    const [activities, setActivities] = useState([])
    const [wsMsg, setWsMsg] = useState('')

    useEffect(()=>{
        fetch(`${API}/health`).then(r=>r.json()).then(setHealth)
        fetch(`${API}/api/activities/`).then(r=>r.json()).then(setActivities)
        // check current session
        fetch(`${API}/api/auth/me`, {credentials: 'include'}).then(r=>r.json()).then(data=>{
            if(data && data.user){ setLoggedIn(true); setUsername(data.user.username) }
        })

        const ws = new WebSocket('ws://localhost:8000/ws')
        ws.onopen = ()=> ws.send('hello from frontend')
        ws.onmessage = (e)=> setWsMsg(e.data)
        return ()=> ws.close()
    }, [])

    const [username, setUsername] = React.useState('')
    const [password, setPassword] = React.useState('')
    const [loggedIn, setLoggedIn] = React.useState(false)
    const [newActivity, setNewActivity] = React.useState('')

    async function createUser(){
        const r = await fetch(`${API}/api/users/`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password})})
        if(r.ok) alert('user created')
        else alert('could not create user')
    }

    async function login(){
        const r = await fetch(`${API}/api/auth/login`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password}), credentials: 'include'})
        if(r.ok) { setLoggedIn(true); alert('logged in') }
        else alert('login failed')
    }

    async function logout(){
        const r = await fetch(`${API}/api/auth/logout`, {method:'POST', credentials: 'include'})
        if(r.ok){ setLoggedIn(false); setUsername(''); alert('logged out') }
    }

    async function createActivity(){
        const r = await fetch(`${API}/api/activities/`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({activity_type:newActivity, confidence:0.5})})
        if(r.ok) { const a = await r.json(); setActivities([a, ...activities]) }
        else alert('activity failed')
    }

    return (
        <div style={{padding:20,fontFamily:'Segoe UI'}}>
            <h1>REPLIKA (Frontend Demo)</h1>

            <section>
                <h3>Health</h3>
                <pre>{JSON.stringify(health,null,2)}</pre>
            </section>

            <section>
                <h3>Account</h3>
                {loggedIn ? (
                    <div>
                        <div>Signed in as <strong>{username}</strong></div>
                        <button onClick={logout}>Logout</button>
                    </div>
                ) : (
                <div>
                    <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="username" />
                    <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="password" type="password" />
                    <button onClick={createUser}>Create</button>
                    <button onClick={login}>Login</button>
                </div>
                )}
            </section>

            <section>
                <h3>Create Activity</h3>
                <input value={newActivity} onChange={e=>setNewActivity(e.target.value)} placeholder="activity type" />
                <button onClick={createActivity}>Create Activity</button>
            </section>

            <section>
                <h3>Activities</h3>
                <ul>
                    {activities.map(a=> <li key={a.id}>{a.activity_type} ({a.confidence})</li>)}
                </ul>
            </section>

            <section>
                <h3>WebSocket</h3>
                <div>{wsMsg}</div>
            </section>
        </div>
    )
}
