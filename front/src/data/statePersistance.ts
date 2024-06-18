const routes = {
  join: 'join/',
  game: 'game/',
}
export const router = {
  getValue: (route: keyof typeof routes) => {
    return location.hash.slice(1).startsWith(route)
      ? location.hash.slice(1 + route.length)
      : null
  },
  setValue: (route: keyof typeof routes, payload: string | null) => {
    if(!payload) return
    location.hash = routes[route] + payload
  },
}
