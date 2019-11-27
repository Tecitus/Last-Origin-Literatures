'use strict'

const path = require('path');
var fastify = require('fastify')({
  logger: true
})
//const AutoLoad = require('fastify-autoload');
//var path = require('path');
var fs = require('fs');
var Sequelize = require('sequelize');
var sequelize = new Sequelize('lastorigin','lao','12345', {
  host: '172.30.1.19',
  dialect: 'postgres',
//  logging: false,
  // SQLite only
  //storage: __dirname+'/../literatures.db'
});
var main = function (fastify) {
  fastify.register(require('fastify-formbody'));
  fastify.register(require('point-of-view'),{
    engine: {
      handlebars: require('handlebars')
    }
  });
  // Loads DB models
  var models = {}
  var files = fs.readdirSync(__dirname+'/models');
  for(var i = 0;i < files.length;i++){
    models[path.basename(files[i],'.js')] = require(__dirname+'/models/'+files[i])(sequelize,Sequelize);
    models[path.basename(files[i],'.js')].sync();
    //console.log(path.basename(files[i]));
  }
  fastify.sgt = {};
  fastify.sgt.models = models;
  fastify.sgt.sq = sequelize;
  // Load routes
  files = fs.readdirSync(__dirname+'/routes');
  for(var i = 0;i < files.length;i++){
    require(__dirname+'/routes/'+files[i])(fastify);
  }
  fastify.listen(40001,'0.0.0.0',(err, address) => {
    //if (err) throw err
    fastify.log.info(`server listening on ${address}`)
  });
}

main(fastify);
