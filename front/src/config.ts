const isProduction = import.meta.env.PROD

const config = {
    isProduction,
    baseUrl: isProduction ? 'https://yakovlitvin.pro/dc-api/' : 'http://127.0.0.1:5000',
}

export default config