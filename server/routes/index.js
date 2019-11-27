const request = require('request');
const cheerio = require('cheerio');
const Sequelize =require('sequelize');
const util = require('util');
const options = {
  uri: 'https://gall.dcinside.com/mgallery/board/view/',
  method: 'GET',
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
  },
  qs: {
    id: 'lastorigin'
  }
};
const fs = require('fs');

var wrapper = async function(fastify,req,rpy){
   var copy = JSON.parse(JSON.stringify(options));
   copy.qs.no = req.body.id;
   request(copy, async (error, response, body)=> {
     var $ = cheerio.load(body);
     var rawname = $('.gall_writer')[0];
     var author = rawname.attribs['data-nick']; //author
     if(rawname.attribs['data-ip'].length>0)
       author+=rawname.attribs['data-ip']; //ip
     var title = $('.title_subject')[0].children[0].data; //title
     var rawtime = $('.gall_date')[0].attribs['title'].split(' ');
     var ymd = rawtime[0].split('-');
     var hms = rawtime[1].split(':');
     var time = new Date(Number(ymd[0]),Number(ymd[1]),Number(ymd[2]),Number(hms[0]),Number(hms[1]),Number(hms[2])); //time
     var url = util.format('https://gall.dcinside.com/mgallery/board/view/?id=lastorigin&no=%s',req.body.id);
     await fastify.sgt.models.archive.create({archiveid: Number(req.body.id),title: title, time: time, author: author, url: url, html: body});
     fs.writeFileSync(__dirname+'/../../html/'+req.body.id+'.html',body);
     rpy.view('/views/index.hbs',{message: '성공적으로 추가되었습니다. 다음날 자정에 업데이트됩니다.'});
   });
}

var wrapper2 = async function(fastify,req,rpy){
   var copy = JSON.parse(JSON.stringify(options));
   copy.qs.no = req.body.id;
   request(copy, async (error, response, body)=> {
     var $ = cheerio.load(body);
     var rawname = $('.gall_writer')[0];
     var author = rawname.attribs['data-nick']; //author
     if(rawname.attribs['data-ip'].length>0)
       author+=rawname.attribs['data-ip']; //ip
     var title = $('.title_subject')[0].children[0].data; //title
     var url = util.format('https://gall.dcinside.com/mgallery/board/view/?id=lastorigin&no=%s',req.body.id);
     var arc = await fastify.sgt.models.archive.findOne({where:{archiveid: Number(req.body.id)}});
     if(arc)
       await arc.destroy();
     await fastify.sgt.models.blacklist.create({archiveid: Number(req.body.id),reason: req.body.reason,title: title, updated: Date.now(), author: author, url: url});
     rpy.view('/views/notliter.hbs',{message: '블랙리스트에 등록되었습니다.'});
   });
}

module.exports = function (fastify){
  fastify.get('/', async(req,rpy)=>{
    rpy.view('/views/index.hbs',{message: ''});
  });

  fastify.post('/', async(req,rpy)=>{
    try{
    var result = await fastify.sgt.models.archive.findOne({where: {archiveid: Number(req.body.id)}});
    if(result)
      rpy.view('/views/index.hbs',{message: '이미 존재합니다.'});
    else
    {
      var black = await fastify.sgt.models.blacklist.findOne({where: {archiveid: Number(req.body.id)}})
      if(black){
        rpy.view('/views/index.hbs',{message: '글 id가 블랙리스트에 있습니다. 사유:'+black.dataValues.reason});
      }
      else{
        wrapper(fastify,req,rpy)
      }
    }
    }
    catch(e){
      console.log(e);
      rpy.view('/views/index.hbs',{message: '에러 발생'});
    }
    return rpy
  });

  fastify.get('/notliter', async(req,rpy)=>{
    rpy.view('/views/notliter.hbs',{message: ''});
  });

  fastify.post('/notliter', async(req,rpy)=>{
    try{
      var result = await fastify.sgt.models.blacklist.findOne({where: {archiveid: Number(req.body.id)}});
      if(result)
        rpy.view('/views/notliter.hbs',{message: '이미 블랙리스트에 있습니다'});
      else{
        wrapper2(fastify,req,rpy);
      }
    }
    catch(e){
      console.log(e);
      rpy.view('/views/notliter.hbs',{message: '에러 발생'});
    }
  });
}
