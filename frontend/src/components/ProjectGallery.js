import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Folder, 
  File, 
  Eye, 
  Code, 
  Download, 
  ExternalLink,
  FolderOpen,
  FileText,
  Image,
  Loader2,
  RefreshCw
} from 'lucide-react';

const ProjectGallery = () => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    setIsLoading(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/generated-projects`);
      const data = await response.json();
      
      if (data.success) {
        setProjects(data.projects);
        setLastUpdate(new Date());
      }
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    
    switch (extension) {
      case 'html':
        return { icon: Code, color: 'text-orange-500 bg-orange-100' };
      case 'css':
        return { icon: Code, color: 'text-blue-500 bg-blue-100' };
      case 'js':
      case 'jsx':
        return { icon: Code, color: 'text-yellow-500 bg-yellow-100' };
      case 'py':
        return { icon: Code, color: 'text-green-500 bg-green-100' };
      case 'json':
        return { icon: FileText, color: 'text-purple-500 bg-purple-100' };
      case 'md':
        return { icon: FileText, color: 'text-gray-500 bg-gray-100' };
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'svg':
        return { icon: Image, color: 'text-pink-500 bg-pink-100' };
      default:
        return { icon: File, color: 'text-gray-500 bg-gray-100' };
    }
  };

  const formatFileSize = (content) => {
    if (!content) return '0 B';
    const bytes = new Blob([content]).size;
    const sizes = ['B', 'KB', 'MB'];
    if (bytes === 0) return '0 B';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div 
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-pink-100 px-4 py-2 rounded-full mb-4">
          <FolderOpen className="w-5 h-5 text-purple-600" />
          <span className="text-purple-700 font-medium">Project Gallery</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Generated Projects
        </h2>
        <p className="text-gray-600">
          Browse and explore all projects created by your AI agents
        </p>
      </motion.div>

      {/* Controls */}
      <motion.div
        className="flex items-center justify-between bg-white rounded-xl p-4 border border-gray-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Folder className="w-4 h-4" />
            <span>{projects.length} projects found</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <span>Last updated: {lastUpdate.toLocaleTimeString()}</span>
          </div>
        </div>
        
        <motion.button
          onClick={fetchProjects}
          disabled={isLoading}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </motion.button>
      </motion.div>

      {/* Projects Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        {isLoading ? (
          <div className="col-span-full flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="w-8 h-8 text-blue-500 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Loading projects...</p>
            </div>
          </div>
        ) : projects.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <FolderOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Projects Found</h3>
            <p className="text-gray-600 mb-4">
              Generate your first project to see it appear here
            </p>
          </div>
        ) : (
          projects.map((project, index) => {
            const { icon: IconComponent, color } = project.type === 'directory' 
              ? { icon: Folder, color: 'text-blue-500 bg-blue-100' }
              : getFileIcon(project.name);

            return (
              <motion.div
                key={index}
                className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all cursor-pointer"
                onClick={() => setSelectedProject(selectedProject === project ? null : project)}
                whileHover={{ y: -4 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
                      <IconComponent className="w-6 h-6" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">
                        {project.name}
                      </h3>
                      <p className="text-sm text-gray-500 capitalize mb-2">
                        {project.type}
                      </p>
                      
                      {project.type === 'file' && (
                        <div className="text-xs text-gray-400">
                          Size: {formatFileSize(project.preview)}
                        </div>
                      )}
                      
                      {project.type === 'directory' && project.files && (
                        <div className="text-xs text-gray-400">
                          {project.files.length} files
                        </div>
                      )}
                    </div>
                    
                    <div className="flex space-x-2">
                      <motion.button
                        className="p-2 text-gray-400 hover:text-blue-500 transition-colors"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        <Eye className="w-4 h-4" />
                      </motion.button>
                    </div>
                  </div>

                  {/* Expanded Content */}
                  {selectedProject === project && (
                    <motion.div
                      className="mt-4 pt-4 border-t border-gray-100"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                    >
                      <div className="space-y-3">
                        <div>
                          <h4 className="text-sm font-medium text-gray-700 mb-2">Path</h4>
                          <p className="text-xs text-gray-500 bg-gray-50 rounded px-2 py-1 font-mono">
                            {project.path}
                          </p>
                        </div>

                        {project.type === 'file' && project.preview && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-2">Preview</h4>
                            <div className="bg-gray-50 rounded-lg p-3 max-h-32 overflow-y-auto">
                              <pre className="text-xs text-gray-600 whitespace-pre-wrap">
                                {project.preview}
                              </pre>
                            </div>
                          </div>
                        )}

                        {project.type === 'directory' && project.files && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-2">
                              Files ({project.files.length})
                            </h4>
                            <div className="space-y-1 max-h-24 overflow-y-auto">
                              {project.files.map((file, fileIndex) => {
                                const { icon: FileIcon, color: fileColor } = getFileIcon(file);
                                return (
                                  <div key={fileIndex} className="flex items-center space-x-2 text-xs">
                                    <div className={`w-4 h-4 rounded flex items-center justify-center ${fileColor}`}>
                                      <FileIcon className="w-2 h-2" />
                                    </div>
                                    <span className="text-gray-600">{file}</span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        )}

                        <div className="flex space-x-2 pt-2">
                          <motion.button
                            className="flex items-center space-x-1 px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            <ExternalLink className="w-3 h-3" />
                            <span>Open</span>
                          </motion.button>
                          
                          <motion.button
                            className="flex items-center space-x-1 px-3 py-1 text-xs bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            <Download className="w-3 h-3" />
                            <span>Download</span>
                          </motion.button>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </div>
              </motion.div>
            );
          })
        )}
      </motion.div>
    </div>
  );
};

export default ProjectGallery;