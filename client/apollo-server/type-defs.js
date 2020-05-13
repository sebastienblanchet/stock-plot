import fs from 'fs'
import path from 'path'

// import schema
export default fs.readFileSync(path.resolve(__dirname, './schema.graphql'), { encoding: 'utf8' })
