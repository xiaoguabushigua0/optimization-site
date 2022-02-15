module.exports = {
    devServer: {
        proxy: {
            '/API': {
                changeOrigin: true,
                target: "http://192.168.1.101:8888",
                pathRewrite: { '^/API': '' }
            },
            '/inverse_dnn': {
                changeOrigin: true,
                target: "http://192.168.1.101:8887",
                pathRewrite: { '^/inverse_dnn': '' }
            },
            '/feature': {
                changeOrigin: true,
                target: "http://192.168.1.101:8886",
                pathRewrite: { '^/feature': '' }
            },
            '/inverse_cnn': {
                changeOrigin: true,
                target: "http://192.168.1.101:8885",
                pathRewrite: { '^/inverse_cnn': '' }
            },
            '/forward_prediction': {
                changeOrigin: true,
                target: "http://192.168.1.101:8884",
                pathRewrite: { '^/forward_prediction': '' }
            },
            '/inverse_hfss': {
                changeOrigin: true,
                target: "http://192.168.1.101:8883",
                pathRewrite: { '^/inverse_hfss': '' }
            },
            '/optimization_ga': {
                changeOrigin: true,
                target: "http://192.168.1.101:8882",
                pathRewrite: { '^/optimization_ga': '' }
            },
            '/forward_opti': {
                changeOrigin: true,
                target: "http://192.168.1.101:8881",
                pathRewrite: { '^/forward_opti': '' }
            },
            '/opti_hfss': {
                changeOrigin: true,
                target: "http://192.168.1.101:8880",
                pathRewrite: { '^/opti_hfss': '' }
            },
            '/optimization_pso': {
                changeOrigin: true,
                target: "http://192.168.1.101:8879",
                pathRewrite: { '^/optimization_pso': '' }
            },
            '/optimization_de': {
                changeOrigin: true,
                target: "http://192.168.1.101:8878",
                pathRewrite: { '^/optimization_de': '' }
            },
        }
    },
    runtimeCompiler: true,
}

