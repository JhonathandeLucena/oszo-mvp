import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUser } from '../contexts/UserContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  HelpCircle, 
  MessageCircle, 
  Phone, 
  Mail, 
  Book,
  Accessibility,
  Volume2,
  Eye,
  Type,
  Contrast,
  Heart,
  User,
  LogOut,
  ArrowLeft,
  Send,
  ChevronDown,
  ChevronRight,
  Play
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { toast } from 'sonner'

const Support = () => {
  const navigate = useNavigate()
  const { user, logout } = useUser()
  const [chatMessage, setChatMessage] = useState('')
  const [supportForm, setSupportForm] = useState({
    subject: '',
    message: '',
    priority: 'medium'
  })
  
  // Estados para configurações de acessibilidade
  const [accessibilitySettings, setAccessibilitySettings] = useState({
    highContrast: false,
    largeText: false,
    screenReader: false,
    reducedMotion: false,
    audioDescriptions: false
  })

  const [openFAQ, setOpenFAQ] = useState(null)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const faqs = [
    {
      id: 1,
      question: 'Como agendar uma consulta?',
      answer: 'Para agendar uma consulta, vá até a página inicial e clique em "Agendar Consulta". Escolha o tipo (presencial ou online), selecione a especialidade, o médico, data e horário desejados.'
    },
    {
      id: 2,
      question: 'Como acessar meus exames?',
      answer: 'Seus exames ficam disponíveis na seção "Histórico Médico". Lá você pode visualizar, baixar e organizar todos os seus documentos médicos.'
    },
    {
      id: 3,
      question: 'Como funciona a teleconsulta?',
      answer: 'A teleconsulta é realizada por videochamada. Você receberá um link por email 30 minutos antes da consulta. Certifique-se de ter uma boa conexão com a internet.'
    },
    {
      id: 4,
      question: 'Posso cancelar uma consulta?',
      answer: 'Sim, você pode cancelar uma consulta com até 24 horas de antecedência sem custos. Para cancelamentos com menos tempo, podem ser aplicadas taxas.'
    },
    {
      id: 5,
      question: 'Como alterar meus dados pessoais?',
      answer: 'Você pode alterar seus dados pessoais clicando no seu avatar no canto superior direito e selecionando "Perfil".'
    },
    {
      id: 6,
      question: 'A plataforma é segura?',
      answer: 'Sim, utilizamos criptografia de ponta a ponta e seguimos todas as normas da LGPD para proteger seus dados médicos.'
    }
  ]

  const tutorialSteps = [
    {
      title: 'Bem-vindo à OSZO',
      description: 'Conheça sua plataforma de saúde digital',
      duration: '2 min'
    },
    {
      title: 'Agendando sua primeira consulta',
      description: 'Aprenda a marcar consultas online e presenciais',
      duration: '3 min'
    },
    {
      title: 'Navegando pelo histórico médico',
      description: 'Como acessar e organizar seus documentos',
      duration: '2 min'
    },
    {
      title: 'Usando a teleconsulta',
      description: 'Guia completo para consultas online',
      duration: '4 min'
    }
  ]

  const handleSendMessage = () => {
    if (chatMessage.trim()) {
      toast.success('Mensagem enviada! Nossa equipe responderá em breve.')
      setChatMessage('')
    }
  }

  const handleSubmitSupport = (e) => {
    e.preventDefault()
    toast.success('Solicitação de suporte enviada com sucesso!')
    setSupportForm({ subject: '', message: '', priority: 'medium' })
  }

  const handleAccessibilityChange = (setting, value) => {
    setAccessibilitySettings(prev => ({
      ...prev,
      [setting]: value
    }))
    
    // Aplicar mudanças na interface
    if (setting === 'highContrast') {
      document.body.classList.toggle('high-contrast', value)
    }
    if (setting === 'largeText') {
      document.body.classList.toggle('large-text', value)
    }
    
    toast.success(`${setting === 'highContrast' ? 'Alto contraste' : 
                   setting === 'largeText' ? 'Texto grande' :
                   setting === 'screenReader' ? 'Leitor de tela' :
                   setting === 'reducedMotion' ? 'Movimento reduzido' :
                   'Descrições de áudio'} ${value ? 'ativado' : 'desativado'}`)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/home')}
                className="mr-4"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Voltar
              </Button>
              <Heart className="h-8 w-8 text-blue-600 mr-2" />
              <span className="text-2xl font-bold text-gray-900">OSZO</span>
            </div>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={user?.avatar} alt={user?.name} />
                    <AvatarFallback>{user?.name?.charAt(0)}</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user?.name}</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user?.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <User className="mr-2 h-4 w-4" />
                  <span>Perfil</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Sair</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Central de Suporte</h1>
          <p className="text-gray-600">
            Encontre ajuda, tutoriais e configure opções de acessibilidade
          </p>
        </div>

        <Tabs defaultValue="help" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="help">Ajuda</TabsTrigger>
            <TabsTrigger value="tutorial">Tutorial</TabsTrigger>
            <TabsTrigger value="contact">Contato</TabsTrigger>
            <TabsTrigger value="accessibility">Acessibilidade</TabsTrigger>
          </TabsList>

          {/* Ajuda */}
          <TabsContent value="help" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <HelpCircle className="h-5 w-5 mr-2" />
                      Perguntas Frequentes
                    </CardTitle>
                    <CardDescription>
                      Encontre respostas para as dúvidas mais comuns
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {faqs.map((faq) => (
                      <Collapsible
                        key={faq.id}
                        open={openFAQ === faq.id}
                        onOpenChange={() => setOpenFAQ(openFAQ === faq.id ? null : faq.id)}
                      >
                        <CollapsibleTrigger asChild>
                          <Button variant="ghost" className="w-full justify-between p-4 h-auto">
                            <span className="text-left font-medium">{faq.question}</span>
                            {openFAQ === faq.id ? (
                              <ChevronDown className="h-4 w-4" />
                            ) : (
                              <ChevronRight className="h-4 w-4" />
                            )}
                          </Button>
                        </CollapsibleTrigger>
                        <CollapsibleContent className="px-4 pb-4">
                          <p className="text-gray-600">{faq.answer}</p>
                        </CollapsibleContent>
                      </Collapsible>
                    ))}
                  </CardContent>
                </Card>
              </div>

              <div>
                <Card>
                  <CardHeader>
                    <CardTitle>Precisa de mais ajuda?</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Button className="w-full" onClick={() => navigate('/support?tab=contact')}>
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Falar com Suporte
                    </Button>
                    <Button variant="outline" className="w-full">
                      <Phone className="h-4 w-4 mr-2" />
                      (11) 3000-0000
                    </Button>
                    <Button variant="outline" className="w-full">
                      <Mail className="h-4 w-4 mr-2" />
                      suporte@oszo.com.br
                    </Button>
                  </CardContent>
                </Card>

                <Card className="mt-6">
                  <CardHeader>
                    <CardTitle>Status do Sistema</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span className="text-sm">Todos os sistemas operacionais</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Tutorial */}
          <TabsContent value="tutorial" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Book className="h-5 w-5 mr-2" />
                  Tutorial Interativo
                </CardTitle>
                <CardDescription>
                  Aprenda a usar todas as funcionalidades da plataforma
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {tutorialSteps.map((step, index) => (
                    <Card key={index} className="cursor-pointer hover:shadow-lg transition-shadow">
                      <CardContent className="p-6">
                        <div className="flex items-start space-x-4">
                          <div className="bg-blue-100 p-2 rounded-lg">
                            <Play className="h-6 w-6 text-blue-600" />
                          </div>
                          <div className="flex-1">
                            <h3 className="font-semibold mb-2">{step.title}</h3>
                            <p className="text-sm text-gray-600 mb-3">{step.description}</p>
                            <Badge variant="outline">{step.duration}</Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Contato */}
          <TabsContent value="contact" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Chat de Suporte</CardTitle>
                  <CardDescription>
                    Fale conosco em tempo real
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="h-64 bg-gray-50 rounded-lg p-4 overflow-y-auto">
                      <div className="space-y-3">
                        <div className="flex items-start space-x-2">
                          <Avatar className="h-6 w-6">
                            <AvatarFallback className="text-xs">S</AvatarFallback>
                          </Avatar>
                          <div className="bg-white p-2 rounded-lg shadow-sm">
                            <p className="text-sm">Olá! Como posso ajudá-lo hoje?</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Input
                        placeholder="Digite sua mensagem..."
                        value={chatMessage}
                        onChange={(e) => setChatMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      />
                      <Button onClick={handleSendMessage}>
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Enviar Solicitação</CardTitle>
                  <CardDescription>
                    Descreva seu problema detalhadamente
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmitSupport} className="space-y-4">
                    <div>
                      <Label htmlFor="subject">Assunto</Label>
                      <Input
                        id="subject"
                        value={supportForm.subject}
                        onChange={(e) => setSupportForm({...supportForm, subject: e.target.value})}
                        placeholder="Descreva brevemente o problema"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="message">Mensagem</Label>
                      <Textarea
                        id="message"
                        value={supportForm.message}
                        onChange={(e) => setSupportForm({...supportForm, message: e.target.value})}
                        placeholder="Descreva o problema em detalhes..."
                        rows={4}
                        required
                      />
                    </div>
                    <Button type="submit" className="w-full">
                      Enviar Solicitação
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Acessibilidade */}
          <TabsContent value="accessibility" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle classN
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)