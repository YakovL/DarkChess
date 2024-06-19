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
  buildHash: (route: keyof typeof routes, payload: string) => {
    return routes[route] + payload
  },
  setValue: function(route: keyof typeof routes, payload: string) {
    location.hash = this.buildHash(route, payload)
  },
  getJoinUrl: function(joinSecret: string) {
    if(!this) return
    return location.origin + location.pathname + '#' + this.buildHash('join', joinSecret)
  },
}
