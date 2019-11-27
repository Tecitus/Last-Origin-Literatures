/* jshint indent: 2 */

module.exports = function(sequelize, DataTypes) {
  return sequelize.define('blacklist', {
    id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      autoIncrement: true,
      primaryKey: true
    },
    archiveid: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    title: {
      type: DataTypes.STRING(256),
      allowNull: false
    },
    author: {
      type: DataTypes.STRING(64),
      allowNull: false
    },
    reason: {
      type: DataTypes.STRING(64),
      allowNull: false
    },
    url: {
      type: DataTypes.STRING(90),
      allowNull: false
    },
    updated: {
      type: DataTypes.DATE,
      allowNull: false
    }
  }, {
    tableName: 'blacklist',
    timestamps: false
  });
};
